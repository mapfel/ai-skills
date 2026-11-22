"""Offline browser for reviewing OCR-recognized photo negative numbers."""
import html
import secrets
import threading
import webbrowser
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlparse

import photos


def rows_for(folder):
    groups = photos.originals(folder)
    found = photos.markers(folder)
    rows = []
    for stem, files in sorted(groups.items()):
        entries = found.get(stem, [])
        rows.append({'stem': stem,
                     'roll': int(photos.SOURCE.fullmatch(stem + '.jpg')['roll']),
                     'files': files,
                     'markers': entries,
                     'number': entries[0][1] if len(entries) == 1 else '',
                     'complete': set(files) == {'original', '_a', '_b'}})
    return rows


def save_numbers(folder, entered):
    rows = rows_for(folder)
    if not rows:
        raise ValueError('Keine Eingabefotos gefunden.')
    errors, desired, seen = [], {}, defaultdict(list)
    for row in rows:
        stem = row['stem']
        number = entered.get(stem, '').strip().upper()
        if not row['complete']:
            errors.append(f'{stem}: Foto-Triplett unvollständig.')
        if not number:
            errors.append(f'{stem}: Negativnummer fehlt.')
            continue
        try:
            number = photos.normalized(number)
        except ValueError as exc:
            errors.append(f'{stem}: {exc}')
            continue
        desired[stem] = folder / f'{stem}_{number}.txt'
        seen[(row['roll'], number)].append(stem)
    for (roll, number), stems in seen.items():
        if len(stems) > 1:
            errors.append(f'Filmrolle {roll}: {number} mehrfach: {", ".join(stems)}')
    if errors:
        raise ValueError('\n'.join(errors))
    old = {path for row in rows for path, _ in row['markers']}
    new = set(desired.values())
    for path in old:
        if path.stat().st_size:
            raise ValueError(f'Marker nicht leer: {path.name}')
    for path in new:
        if path.exists() and path not in old:
            raise ValueError(f'Dateikonflikt: {path.name}')
    created = []
    try:
        for path in sorted(new - old):
            path.touch(exist_ok=False)
            created.append(path)
    except OSError:
        for path in created:
            path.unlink(missing_ok=True)
        raise
    for path in old - new:
        path.unlink()
    photos.check(folder)
    return len(rows)


CSS = '''
:root{font-family:system-ui,sans-serif;color-scheme:light}
body{margin:0 auto;max-width:1160px;padding:24px;background:#f5f7fb;color:#1c2735}
h1{margin:0 0 8px}p{line-height:1.5}
.banner{background:#fff;border:1px solid #dae1eb;border-radius:10px;padding:16px;margin:14px 0;white-space:pre-line}
.error{color:#8f2121;background:#ffeded}.ok{color:#145c3d;background:#e6f7ed}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.photo{background:white;border:1px solid #dde3ea;border-radius:10px;padding:14px;min-width:0}
.warn{border:2px solid #b45309}
.photo img{display:block;width:100%;height:220px;object-fit:contain;background:#eef1f5;border-radius:6px}
.photo h3{font-size:15px;overflow-wrap:anywhere}
label{display:block;margin:10px 0 5px;font-weight:600}
input[type=text]{box-sizing:border-box;width:100%;padding:10px;border:1px solid #8b9ab0;border-radius:5px;font-size:18px}
small{color:#475569}button{padding:12px 20px;border:0;background:#124c86;color:white;border-radius:7px;cursor:pointer;font-weight:600}
.actions{position:sticky;bottom:0;background:#f5f7fb;padding:12px 0;border-top:1px solid #cdd5e0;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
'''


def render(folder, rows, token, message='', error=False):
    parts = ['<!doctype html><html lang="de"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Negativnummern prüfen</title><style>', CSS, '</style></head><body>',
             '<h1>Negativnummern prüfen</h1>',
             '<p>Scans werden ausschließlich lokal angezeigt. Nummern korrigieren,',
             'danach gemeinsam prüfen und speichern (0–36 oder 0A–36A).</p>',
             f'<p><strong>{len(rows)} Fotos</strong> in {html.escape(str(folder))}</p>']
    if message:
        kind = 'error' if error else 'ok'
        parts.append(f'<div class="banner {kind}" role="status">{html.escape(message)}</div>')
    parts.append('<form method="post" action="/save"><div class="grid">')
    for i, row in enumerate(rows):
        stem = row['stem']
        name = html.escape(stem)
        value = html.escape(row['number'], quote=True)
        flags = []
        if not row['complete']:
            flags.append('Triplett unvollständig')
        if len(row['markers']) > 1:
            flags.append('Mehrere Marker')
        elif not value:
            flags.append('OCR-Nummer fehlt')
        cls = ' warn' if flags else ''
        parts.append(f'<section class="photo{cls}"><h3>{name}</h3>')
        if '_b' in row['files']:
            url = '/image?stem=' + quote(stem, safe='')
            parts.append(f'<a href="{url}" target="_blank" rel="noopener"><img loading="lazy" src="{url}" alt="Rückseite von {name}"></a>')
        else:
            parts.append('<p>Kein Rückseitenscan vorhanden</p>')
        parts.append(f'<label for="v{i}">Negativnummer · Filmrolle {row["roll"]}</label>')
        parts.append(f'<input type="text" id="v{i}" name="negative:{html.escape(stem, quote=True)}" value="{value}" '
                     'pattern="(?:[0-9]|[12][0-9]|3[0-6])[aA]?" required autocomplete="off" placeholder="z. B. 1A">')
        parts.append(f'<small>{html.escape(" · ".join(flags)) if flags else "Bitte kontrollieren"}</small></section>')
    parts.append(f'</div><div class="actions"><input type="hidden" name="token" value="{token}">'
                 '<button type="submit">Alle Nummern prüfen &amp; speichern</button>'
                 '<small>Die JPG-Dateien bleiben unverändert.</small></div></form></body></html>')
    return ''.join(parts).encode('utf-8')


def serve(folder, port=0, open_browser=True):
    if not rows_for(folder):
        raise ValueError('Keine Eingabedateien vorhanden.')
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def send_bytes(self, status, data, content_type):
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy',
                             "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path == '/':
                self.send_bytes(200, render(folder, rows_for(folder), token), 'text/html; charset=utf-8')
            elif parsed.path == '/image':
                stem = parse_qs(parsed.query).get('stem', [''])[0]
                row = next((r for r in rows_for(folder) if r['stem'] == stem), None)
                if row is None or '_b' not in row['files']:
                    self.send_error(404)
                    return
                try:
                    self.send_bytes(200, row['files']['_b'].read_bytes(), 'image/jpeg')
                except OSError:
                    self.send_error(404)
            else:
                self.send_error(404)

        def do_POST(self):
            if self.path != '/save':
                self.send_error(404)
                return
            length = int(self.headers.get('Content-Length', '-1'))
            if length < 0 or length > 1_000_000:
                self.send_error(413)
                return
            form = parse_qs(self.rfile.read(length).decode('utf-8'), keep_blank_values=True)
            if form.get('token') != [token]:
                self.send_error(403)
                return
            entered = {key[len('negative:'):]: values[0]
                       for key, values in form.items()
                       if key.startswith('negative:') and len(values) == 1}
            try:
                count = save_numbers(folder, entered)
                message, error = f'{count} Nummern gespeichert. Nächste Schritte: rename, reorganize, missing.', False
            except (ValueError, OSError) as exc:
                message, error = str(exc), True
            rows = rows_for(folder)
            if error:
                for row in rows:
                    if row['stem'] in entered:
                        row['number'] = entered[row['stem']]
            self.send_bytes(422 if error else 200,
                            render(folder, rows, token, message, error),
                            'text/html; charset=utf-8')

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    address = f'http://127.0.0.1:{server.server_port}/'
    print(f'Lokale Prüfansicht: {address}', flush=True)
    print('Beenden mit Strg+C. Keine Bilder werden ins Internet übertragen.', flush=True)
    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(address)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
