#!/usr/bin/env python3
"""Sort duplex scanned photo triplets by OCR negative number."""
import argparse
import csv
import io
import re
import subprocess
import sys
import uuid
from collections import defaultdict
from pathlib import Path

SOURCE = re.compile(r'^(?P<date>\d{8})\.(?P<context>.+)-(?P<roll>\d+)_(?P<seq>\d+)(?P<kind>_a|_b)?\.jpg$', re.I)
MARKER = re.compile(r'^(?P<stem>\d{8}\..+-\d+_\d+)_(?P<negative>\d{1,2}A?)\.txt$', re.I)
RENAMED = re.compile(r'^(?P<roll>\d+)_(?P<negative>\d{1,2}A?)(?P<kind>_a|_b)?\.jpg$', re.I)
FINAL = re.compile(r'^(?P<roll>\d+)_(?P<negative>\d{1,2}A?)\.jpg$', re.I)
NEG_TOKEN = re.compile(r'\bNEG(?:ATIV)?\s*(?:\.|:|#|-)?\s*(?:NR\.?\s*)?(\d{1,2})\s*(A)?\b', re.I)


def fail(message):
    raise ValueError(message)


def normalized(value):
    match = re.fullmatch(r'(\d{1,2})(A?)', value.upper())
    if not match or int(match[1]) > 36:
        fail(f'Ungültige Negativnummer: {value} (0–36, optional A)')
    return f'{int(match[1])}{match[2]}'


def originals(folder):
    groups = defaultdict(dict)
    for path in sorted(folder.iterdir()):
        if not path.is_file() or not (match := SOURCE.fullmatch(path.name)):
            continue
        suffix = match['kind'] or 'original'
        stem = path.stem[:-2] if match['kind'] else path.stem
        if suffix in groups[stem]:
            fail(f'Doppelte Scan-Datei: {stem}/{suffix}')
        groups[stem][suffix] = path
    return dict(groups)


def markers(folder):
    found = defaultdict(list)
    for path in folder.iterdir():
        if path.is_file() and (match := MARKER.fullmatch(path.name)):
            found[match['stem']].append((path, normalized(match['negative'])))
    return found


def scan_negative(path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError:
        fail('Pillow fehlt: python -m pip install Pillow')
    guesses = set()
    try:
        with Image.open(path) as source:
            image = ImageEnhance.Contrast(ImageOps.autocontrast(ImageOps.grayscale(source))).enhance(1.6)
            for angle in (0, 90, 180, 270):
                rotated = image.rotate(angle, expand=True)
                buffer = io.BytesIO()
                rotated.save(buffer, 'PNG')
                for mode in (6, 11):
                    result = subprocess.run(
                        ['tesseract', 'stdin', 'stdout', '--psm', str(mode)],
                        input=buffer.getvalue(), capture_output=True, timeout=45)
                    if result.returncode:
                        fail(f'OCR-Fehler bei {path.name}: {result.stderr.decode(errors="replace")[:160]}')
                    for match in NEG_TOKEN.finditer(result.stdout.decode(errors='replace')):
                        try:
                            guesses.add(normalized(match[1] + (match[2] or '')))
                        except ValueError:
                            pass
    except FileNotFoundError:
        fail('Tesseract nicht im PATH gefunden.')
    except subprocess.TimeoutExpired:
        fail(f'OCR-Zeitüberschreitung: {path.name}')
    return guesses


def issues(groups, existing):
    problems, used = [], defaultdict(list)
    for stem, files in groups.items():
        if set(files) != {'original', '_a', '_b'}:
            problems.append((stem, f'Unvollständiges Triplett: {sorted(files)}'))
        entries = existing.get(stem, [])
        if len(entries) != 1:
            problems.append((stem, f'Erwartet genau einen Marker, gefunden: {len(entries)}'))
        else:
            if entries[0][0].stat().st_size:
                problems.append((stem, 'Marker ist nicht leer'))
            roll = int(SOURCE.fullmatch(stem + '.jpg')['roll'])
            used[(roll, entries[0][1])].append(stem)
    for (roll, negative), stems in used.items():
        if len(stems) > 1:
            problems.append((f'{roll}_{negative}', 'Doppelt: ' + ', '.join(stems)))
    for stem in existing.keys() - groups.keys():
        problems.append((stem, 'Marker ohne zugehöriges Foto'))
    return problems


def check(folder):
    groups = originals(folder)
    if not groups:
        fail('Keine Eingabefotos gefunden.')
    problems = issues(groups, markers(folder))
    report = folder / 'OCR_REVIEW.tsv'
    if problems:
        with report.open('w', encoding='utf-8', newline='') as output:
            writer = csv.writer(output, delimiter='\t')
            writer.writerow(['Datei/Negativ', 'Problem'])
            writer.writerows(problems)
        for stem, reason in problems:
            print(f'  {stem}: {reason}')
        print(f'Korrektur erforderlich: {report.name}')
        return False
    report.unlink(missing_ok=True)
    print('Prüfung erfolgreich.')
    return True


def ocr(folder):
    groups = originals(folder)
    if not groups:
        fail('Keine Eingabefotos gefunden.')
    known = markers(folder)
    for stem, files in groups.items():
        if known.get(stem):
            continue  # Manual corrections take priority.
        if '_b' not in files:
            continue
        try:
            guesses = scan_negative(files['_b'])
        except (ValueError, OSError) as exc:
            print(f'{stem}: {exc}')
            continue
        if len(guesses) == 1:
            number = next(iter(guesses))
            (folder / f'{stem}_{number}.txt').touch(exist_ok=False)
            print(f'{stem}: {number}')
        else:
            print(f'{stem}: uneindeutige OCR: {sorted(guesses)}')
    return check(folder)


def move_all(moves):
    moves = [(a, b) for a, b in moves if a != b]
    sources = {a for a, _ in moves}
    targets = [b for _, b in moves]
    if len(targets) != len(set(targets)):
        fail('Mehrere Quellen haben denselben Zielnamen.')
    for source, target in moves:
        if not source.is_file():
            fail(f'Quelle fehlt: {source}')
        if target.exists() and target not in sources:
            fail(f'Ziel existiert bereits: {target}')
    staged, done = [], []
    try:
        for source, target in moves:
            temp = source.with_name(f'.photo-sort-{uuid.uuid4().hex}.tmp')
            source.rename(temp)
            staged.append((source, temp, target))
        for source, temp, target in staged:
            target.parent.mkdir(parents=True, exist_ok=True)
            temp.rename(target)
            done.append((source, target))
    except Exception:
        for source, target in reversed(done):
            if target.exists():
                target.rename(source)
        for source, temp, _ in reversed(staged):
            if temp.exists():
                temp.rename(source)
        raise


def rename(folder):
    if not check(folder):
        fail('Zuerst OCR-Fehler beheben.')
    moves = []
    existing = markers(folder)
    for stem, files in originals(folder).items():
        roll = int(SOURCE.fullmatch(stem + '.jpg')['roll'])
        number = existing[stem][0][1]
        prefix = f'{roll}_{number}'
        for kind, file in files.items():
            moves.append((file, folder / f'{prefix}{"" if kind == "original" else kind}.jpg'))
        moves.append((existing[stem][0][0], folder / f'{prefix}.txt'))
    move_all(moves)
    print(f'{len(moves)} Dateien umbenannt.')


def reorganize(folder):
    groups = defaultdict(dict)
    for path in folder.iterdir():
        if path.is_file() and (match := RENAMED.fullmatch(path.name)):
            prefix = f'{int(match["roll"])}_{normalized(match["negative"])}'
            kind = match['kind'] or 'original'
            if kind in groups[prefix]:
                fail(f'Doppelter Dateityp: {prefix}/{kind}')
            groups[prefix][kind] = path
    if not groups:
        fail('Keine umbenannten Tripletts vorhanden.')
    moves, to_delete = [], []
    for prefix, files in groups.items():
        if set(files) != {'original', '_a', '_b'}:
            fail(f'Triplett unvollständig: {prefix}')
        marker = folder / f'{prefix}.txt'
        if not marker.is_file() or marker.stat().st_size:
            fail(f'Leerer Marker fehlt: {marker}')
        moves.extend(((files['original'], folder / 'Originale' / f'{prefix}.jpg'),
                      (files['_b'], folder / 'Originale' / f'{prefix}_b.jpg'),
                      (files['_a'], folder / f'{prefix}.jpg')))
        to_delete.append(marker)
    move_all(moves)
    for marker in to_delete:
        marker.unlink()
    print(f'{len(groups)} Tripletts reorganisiert.')


def missing(folder, series):
    root = folder / 'Originale'
    if not root.is_dir():
        fail('Originale-Ordner fehlt.')
    found = defaultdict(set)
    for path in root.iterdir():
        if path.is_file() and (match := FINAL.fullmatch(path.name)):
            found[int(match['roll'])].add(normalized(match['negative']))
    if not found:
        fail('Keine Originalbilder gefunden.')
    planned = []
    for roll, existing in found.items():
        kinds = {'a' if value.endswith('A') else 'plain' for value in existing}
        if series == 'auto':
            if len(kinds) != 1:
                fail(f'Filmrolle {roll}: A-/Nicht-A-Nummern gemischt.')
            kind = next(iter(kinds))
        else:
            kind = series
            if kinds != {kind}:
                fail(f'Filmrolle {roll}: vorhandenes Schema {kinds} passt nicht zu {kind}.')
        for n in range(37):
            number = f'{n}{"A" if kind == "a" else ""}'
            if number not in existing:
                target = root / f'{roll}_{number}.txt'
                if target.exists() and target.read_text(encoding='utf-8') != 'Missing':
                    fail(f'Konflikt mit vorhandenem Platzhalter: {target}')
                if not target.exists():
                    planned.append(target)
    for target in planned:
        target.write_text('Missing', encoding='utf-8')
    print(f'{len(planned)} Missing-Platzhalter angelegt.')


def main():
    parser = argparse.ArgumentParser(description='Duplex-Fotos nach Negativnummer sortieren')
    parser.add_argument('step', choices=('ocr', 'review', 'check', 'rename', 'reorganize', 'missing'))
    parser.add_argument('directory', type=Path)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--port', type=int, default=0)
    parser.add_argument('--series', choices=('auto', 'plain', 'a'), default='auto')
    args = parser.parse_args()
    folder = args.directory.resolve()
    if not folder.is_dir():
        parser.error(f'Verzeichnis existiert nicht: {folder}')
    try:
        if args.step == 'review':
            from review_ui import serve
            serve(folder, port=args.port, open_browser=not args.no_browser)
            return 0
        steps = {'ocr': lambda: ocr(folder),
                 'check': lambda: check(folder),
                 'rename': lambda: rename(folder),
                 'reorganize': lambda: reorganize(folder),
                 'missing': lambda: missing(folder, args.series)}
        result = steps[args.step]()
        return 2 if result is False else 0
    except (ValueError, OSError) as exc:
        print(f'FEHLER: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
