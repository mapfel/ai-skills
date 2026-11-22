# Foto-Negativsortierung

Organisiert mit Epson oder anderen Duplex-Fotoscannern digitalisierte Fotos anhand ihrer auf der Rückseite erkannten Negativnummer. Das Verfahren bewahrt die unveränderten Originalscans getrennt von optimierten Vorderseiten auf.

## Installation

- Python 3.10 oder neuer
- Tesseract OCR im `PATH`
- `python -m pip install Pillow`

## Verwendung

```powershell
python scripts/photos.py ocr "D:\\Fotos\\20020822.Safaga"
python scripts/photos.py review "D:\\Fotos\\20020822.Safaga"
python scripts/photos.py check "D:\\Fotos\\20020822.Safaga"
python scripts/photos.py rename "D:\\Fotos\\20020822.Safaga"
python scripts/photos.py reorganize "D:\\Fotos\\20020822.Safaga"
python scripts/photos.py missing "D:\\Fotos\\20020822.Safaga"
```

Vor dem ersten Lauf ein Backup anlegen. Fehlerhafte oder doppelte Negativnummern müssen in der lokalen Prüfansicht berichtigt werden. Die einzelnen Schritte dürfen nicht bei unbehobenen Fehlern fortgesetzt werden.

## Ergebnis

Im Hauptordner liegen die optimierten Fotos wie `1_1A.jpg`. Im Unterordner `Originale` liegen das Original `1_1A.jpg`, der Rückseitenscan `1_1A_b.jpg` sowie für fehlende Negative TXT-Dateien mit Inhalt `Missing`.

Mit `--series plain` oder `--series a` lässt sich das Nummernschema für den letzten Schritt festlegen. Bei `--series auto` muss jede Rolle eindeutig zuzuordnen sein.
