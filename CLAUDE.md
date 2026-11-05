# RitterAldebert – Homepage

Persönliche Homepage im Stil einer klassischen Tageszeitung (Vorbild: New York Times).
Inhalte: **Artikel/Blog** (`artikel/`). Rubrik **Projekte** ist vorbereitet, aber derzeit ausgeblendet (noch keine Projekte).
Reines HTML/CSS, **kein Build-Schritt, kein Framework, kein npm**. Hosting: GitHub Pages
aus Branch `main`, Ordner `/` (root). URL: `https://<github-name>.github.io/RitterAldebert/`.

## Struktur
```
index.html            Startseite (Titelseite der „Zeitung“)
impressum.html        Impressum (§ 5 DDG / § 18 MStV) – in JEDEM Footer verlinken
datenschutz.html      Datenschutzerklärung – in JEDEM Footer verlinken; bei neuen Diensten anpassen
assets/fonts/         lokal gehostete Schriften (OFL, Lizenz in LIZENZ.txt), eingebunden über assets/css/fonts.css
artikel/index.html    Archiv aller Artikel (neueste oben)
artikel/<slug>.html   ein Artikel pro Datei, slug = kleinbuchstaben-mit-bindestrich
projekte/             (derzeit leer) – erst mit dem ersten echten Projekt anlegen
assets/css/style.css  EINZIGES Stylesheet, alle Farben/Schriften als CSS-Variablen
assets/img/           Bilder, Unterordner pro Artikel/Projekt
vorlagen/             Kopiervorlagen – nie verlinken, nie direkt bearbeiten ohne Auftrag
docs/design.md        Designsystem – VOR jeder gestalterischen Änderung lesen
docs/recherche/       Wissensbasis für Artikel – Fakten nur MIT Quellenangabe übernehmen,
                      „unklar“ markierte Punkte nicht als Tatsache schreiben
RAW/                  Quelldokumente (PDFs), per .gitignore NICHT veröffentlicht
scripts/check_links.py  prüft alle lokalen Links und Bildpfade
```

## Arbeitsregeln
1. **Erst denken:** Annahmen nennen, bei Unklarheit fragen statt raten. Gibt es einen einfacheren Weg, ihn vorschlagen.
2. **Einfach halten:** Nur bauen, was verlangt ist. Kein JavaScript, wenn HTML/CSS reicht. Keine neuen Abhängigkeiten oder Frameworks.
3. **Gezielt ändern:** Nur das Nötige anfassen, bestehenden Stil übernehmen. Unbeteiligte Mängel melden, nicht stillschweigend „reparieren“.
4. **Überprüfbar arbeiten:** Vor der Arbeit festlegen, woran man Erfolg erkennt; am Ende prüfen (siehe „Prüfen“).

## Gestaltung (Kurzfassung – Details in docs/design.md)
- Schwarz auf Weiß, Farbe nur für Links (`--link`) und sehr sparsam.
- Serifenschriften für Überschriften und Fließtext; serifenlose nur für Rubriken, Datum, Bildunterschriften.
- Trennung durch Haarlinien (1px `--rule`) statt Schatten, Rundungen oder Kästen.
- Spaltenraster mit CSS Grid; auf dem Handy einspaltig.
- Keine Effekthascherei: keine Verläufe, keine Animationen außer dezenten Hover-Unterstreichungen.
- Nur die Variablen aus `style.css` verwenden, keine neuen Farbwerte inline.

## Technische Regeln
- **Keine externen Ressourcen** (Datenschutz): keine Google Fonts, CDNs, Embeds (YouTube, Karten), Tracker oder Cookies. Alles lokal ausliefern. Wer das ändert, muss `datenschutz.html` anpassen.
- **Alle Links und Pfade relativ** (`../assets/css/style.css`), nie mit `/` beginnen – die Seite läuft unter dem Unterpfad `/RitterAldebert/`.
- Semantisches HTML (`header`, `nav`, `main`, `article`, `figure`, `time datetime="YYYY-MM-DD"`), `lang="de"`.
- Jede Seite: eigener `<title>`, `<meta name="description">`, gleicher Kopf und Fuß wie `index.html`.
- Bilder: max. 1600px breit, JPG/WebP unter ~300 KB, immer `alt`, `width`/`height`, `loading="lazy"` (außer Aufmacherbild).
- Datumsformat sichtbar: „5. November 2026“.

## Abläufe
**Neuer Artikel:** `vorlagen/artikel.html` → `artikel/<slug>.html` kopieren, Platzhalter `{{…}}` ersetzen.
**Autor ist immer Jens Higgen** (Autorenzeile „Von Jens Higgen · Datum“, steht fest in der Vorlage; Fotos: „Foto: Jens Higgen“, sofern nicht anders angegeben).
**Jeder Blogbeitrag braucht die Teilen-Leiste** (oben nach der Autorenzeile und am Ende: `<div class="share"></div>` / `<div class="share share-end"></div>` + `assets/js/teilen.js`) – ist in der Vorlage enthalten, nie entfernen. Keine Social-Media-Widgets von Dritten.
Danach verlinken: (a) oben in `artikel/index.html`, (b) auf `index.html` als Aufmacher bzw. in die Spalten –
der älteste Startseiten-Teaser rutscht dafür heraus (bleibt im Archiv).

**Neues Projekt:** `vorlagen/projekt.html` → `projekte/<slug>.html`, Bilder nach `assets/img/<slug>/`.
Beim ERSTEN Projekt zusätzlich `projekte/index.html` (Galerie) anlegen und „Projekte“ wieder in Navigation und Fußzeile aller Seiten + `vorlagen/artikel.html` aufnehmen.
**Keine Platzhalter-Inhalte veröffentlichen** (keine Beispielartikel, -projekte oder -bilder).

## Prüfen (vor jedem Veröffentlichen)
```
python3 scripts/check_links.py          # muss "OK" melden
python3 -m http.server 8000             # dann http://localhost:8000 öffnen
```
Startseite, geänderte Seite und Galerie ansehen, auch bei 375px Breite (Handy).

## Veröffentlichen
```
git add -A && git commit -m "<was geändert wurde>" && git push
```
Claude committet und pusht **nur auf ausdrückliche Anweisung**. GitHub Pages ist nach ca. 1 Minute aktuell.
