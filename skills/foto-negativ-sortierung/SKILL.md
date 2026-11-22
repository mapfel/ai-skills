---
name: foto-negativ-sortierung
description: Organisiert duplex gescannte Fotos anhand der per OCR erkannten Negativnummern, inklusive lokaler Prüfansicht, Duplikatkontrolle und Platzhaltern für fehlende Negative.
---

# Foto-Negativsortierung

## Wann verwenden?
Wenn ein Verzeichnis pro Foto drei JPEGs enthält: Original, optimierte Vorderseite (`_a`) und Rückseite (`_b`). Auf der Rückseite steht eine Negativnummer im Bereich 0–36, optional mit Suffix A (etwa `Neg.1A`).

## Namenskonventionen
Eingang: `YYYYMMDD.Kontext-Stapel_Scan.jpg`, `..._a.jpg`, `..._b.jpg`; Beispiel `20020822.Safaga-1_0001.jpg`.
Nach OCR: temporäre, **leere** Markerdatei `20020822.Safaga-1_0001_1A.txt`.
Nach Umbenennung: `1_1A.jpg`, `1_1A_a.jpg`, `1_1A_b.jpg`, `1_1A.txt`.
Endergebnis: Hauptordner `1_1A.jpg` (optimierte Version); `Originale/1_1A.jpg` und `Originale/1_1A_b.jpg`; fehlende Negative als `Originale/1_2A.txt` mit Inhalt `Missing`.

**Verwende zwischen Stapelnummer und Negativnummer einen Unterstrich** (`1_1A`) und entferne `_a` nur von optimierten Fotos im Hauptordner.

## Durchführung
1. Zunächst Backup empfehlen. Nur auf dem explizit genannten Verzeichnis arbeiten, keine rekursive Suche. Niemals Fotos neu kodieren.
2. Mit `python scripts/photos.py ocr "<ordner>"` Negativnummern aus den Rückseiten lesen und Marker erzeugen. Im Zweifel nicht raten; unerkannte, mehrdeutige oder doppelte Nummern melden.
3. Mit `python scripts/photos.py review "<ordner>"` die lokale Browser-Prüfansicht öffnen. Falsche/fehlende Nummern korrigieren. Der Browser bindet ausschließlich an 127.0.0.1.
4. Mit `python scripts/photos.py check "<ordner>"` Vollständigkeit (alle drei JPGs), eindeutige Nummern innerhalb jeder Filmrolle und genau einen Marker pro Foto prüfen. Bei Fehlern **vor Änderungen stoppen**.
5. Mit `python scripts/photos.py rename "<ordner>"` die Dateien umbenennen. Bestehende Ziele niemals überschreiben.
6. Mit `python scripts/photos.py reorganize "<ordner>"` Originale und Rückseiten nach `Originale` verschieben, optimierte Bilder ohne Suffix im Hauptordner lassen und temporäre TXT-Dateien entfernen.
7. Mit `python scripts/photos.py missing "<ordner>"` für jede identifizierte Filmrolle alle fehlenden Nummern von 0 bis 36 bzw. 0A bis 36A als `Missing`-TXT markieren. Gemischte A-/Nicht-A-Filmrollen nicht automatisch interpretieren; Entscheidung einholen.

## Sicherheitsanforderungen
- Keine vorhandene Datei stillschweigend überschreiben oder löschen, außer leeren, eindeutig zugeordneten temporären Markern nach erfolgreicher Umorganisation.
- Alle Zielnamen und Konflikte vor dem Umbenennen prüfen; bei Fehlern abbrechen.
- Bei fehlendem oder mehrdeutigem OCR-Ergebnis keine Nummer erfinden.
- OCR kann falsch liegen: Nutzer zur Sichtprüfung auffordern.
- Gleiche Negativnummern in unterschiedlichen Filmrollen sind erlaubt, innerhalb einer Filmrolle nicht.
- Von Bildern nur die Dateipfade ändern, nie die Bildinhalte.
- Jede Stufe getrennt ausführbar halten und mit Fehlerstatus enden, wenn manuelles Eingreifen nötig ist.

## Abhängigkeiten
Python 3.10+, Pillow (`python -m pip install Pillow`), Tesseract OCR als Kommando `tesseract` im PATH. Für die Browser-Prüfansicht wird nur die Python-Standardbibliothek benötigt. Details: [README.md](README.md).
