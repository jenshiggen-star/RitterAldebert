#!/usr/bin/env python3
"""Prüft alle lokalen href/src-Ziele in den HTML-Dateien (ohne vorlagen/).
Meldet fehlende Ziele und absolute Pfade (/...), die unter GitHub Pages brechen."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATTR = re.compile(r'(?:href|src)="([^"]+)"')
fehler = []
for html in sorted(ROOT.rglob("*.html")):
    rel = html.relative_to(ROOT)
    if rel.parts[0] in ("vorlagen", ".git", "node_modules"):
        continue
    text = html.read_text(encoding="utf-8")
    if "{{" in text:
        fehler.append(f"{rel}: enthält noch Platzhalter {{{{…}}}}")
    for ziel in ATTR.findall(text):
        if re.match(r"^(https?:|mailto:|tel:|#|data:)", ziel):
            continue
        if ziel.startswith("/"):
            fehler.append(f"{rel}: absoluter Pfad '{ziel}' – bitte relativ")
            continue
        pfad = (html.parent / ziel.split("#")[0].split("?")[0]).resolve()
        if not pfad.exists():
            fehler.append(f"{rel}: Ziel fehlt '{ziel}'")

if fehler:
    print("\n".join(fehler))
    sys.exit(1)
print("OK – alle lokalen Links und Bilder gefunden.")
