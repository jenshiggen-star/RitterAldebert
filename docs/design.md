# Designsystem RitterAldebert

Leitbild: die gedruckte Titelseite einer großen Tageszeitung – ruhig, dicht, typografisch.
Angelehnt an die Anmutung der New York Times, **ohne** deren Logo, Namen oder Schriften zu kopieren.

## Schriften (lokal in `assets/fonts/`, eingebunden über `assets/css/fonts.css` – NICHT von Google laden)
| Rolle | Schrift | Variable |
|---|---|---|
| Zeitungskopf (Masthead) | UnifrakturMaguntia (Fraktur – passt zum „Ritter“) | `--font-masthead` |
| Überschriften | Playfair Display 700/900 | `--font-headline` |
| Fließtext, Teaser | Source Serif 4 400/600, kursiv | `--font-body` |
| Rubriken, Datum, Bildunterschrift, Navigation | Libre Franklin 400/600 | `--font-meta` |

Größen: Masthead `clamp(2.6rem, 8vw, 5.5rem)` · Aufmacher-Überschrift `clamp(1.8rem, 4vw, 2.75rem)` ·
Spalten-Überschrift 1.25rem · Fließtext 1.125rem / Zeilenhöhe 1.6 · Meta 0.75rem, Großbuchstaben, Sperrung 0.06em.

## Farben
| Variable | Wert | Einsatz |
|---|---|---|
| `--ink` | #121212 | Text, dicke Linien |
| `--paper` | #ffffff | Hintergrund |
| `--muted` | #5a5a5a | Datum, Autor, Bildunterschrift |
| `--rule` | #dfdfdf | Haarlinien |
| `--link` | #326891 | Links im Fließtext |

## Linien
- Unter dem Masthead: doppelte Linie (`border-bottom: 3px double var(--ink)`).
- Zwischen Spalten: 1px `--rule` als `border-left`.
- Zwischen Teasern: 1px `--rule`.

## Layout
- Seitenbreite max. 1200px, Rand 16px (Handy) bis 32px.
- **Startseite:** Kopfzeile (Datum links, Ort/Ausgabe rechts) → Masthead → Rubrikenleiste →
  Raster `2fr 1fr 1fr`: links Aufmacher mit Bild, rechts zwei Teaser-Spalten. Darunter „Aus der Werkstatt“ (Projekte).
- **Artikel:** Lesespalte max. 640px, zentriert; Rubrik → Überschrift → Unterzeile (kursiv) → Autor/Datum → Bild → Text.
  Erster Absatz mit Initiale (Drop Cap) in der Headline-Schrift.
- **Galerie:** `repeat(auto-fill, minmax(260px, 1fr))`, Bilder 4:3, Unterschrift in Meta-Schrift.
- Unter 760px: alles einspaltig, Spaltenlinien entfallen.

## Grafiken
- Eigene, schematische Grafiken statt fremder Pläne. Pläne von Architekten, WBG usw. **nicht** abbilden (Urheberrecht), sondern Fakten abstrahieren.
- Umsetzung: Inline-SVG oder HTML/CSS im Artikel (`figure.graphic` mit `.g-title`, `.g-sub`, `figcaption`); Karten als SVG-Datei in `assets/img/<slug>/`.
- Farben: nur die Variablen; `--accent` (#a8442a) ausschließlich für „neu / geplant / jetzt“.
- Jede Grafik: Titel, Untertitel, Quellenzeile; `role="img"` + `<title>`/`<desc>` bzw. `alt`.
- Mobil prüfen (390 px): Schrift in der Grafik mindestens ca. 10 px. Karten haben eine eigene Mobil-Variante (`<picture>`, `max-width: 600px`).
- Kartengrundlage OpenStreetMap: immer „© OpenStreetMap-Mitwirkende (ODbL)“ angeben. Generator: `scripts/make_lageskizze.py` (Rohdaten in `RAW/daten/osm_*.json`).
- Keine erfundenen Maße/Zahlen; Abschätzungen und Platzhalter („Messung folgt“) sichtbar kennzeichnen.

## Barrierefreiheit
- Kontrast mind. 4.5:1 (alle Tokens erfüllen das auf Weiß).
- Sichtbarer Fokus: `outline: 2px solid var(--ink); outline-offset: 2px`.
- Links im Fließtext unterstrichen; Überschriften-Links erst beim Hover.
- Bilder immer mit sinnvollem `alt`; rein dekorative mit `alt=""`.
