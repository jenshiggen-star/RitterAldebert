"""Erzeugt die Skizze „Scherbsgraben an der Ritter-von-Aldebert-Straße“ als SVG aus OSM-Daten.
Aufruf: python3 -I scripts/make_scherbsgraben.py RAW/daten/osm_ritter-aldebert_2026-11-05.json out.svg [mobil]
Desktop: assets/img/scherbsgraben/abschnitt.svg · Mobil: abschnitt-mobil.svg
Nummern 1–4 werden im Artikel als HTML-Legende erklärt.
"""
import json, math, sys

src, out = sys.argv[1], sys.argv[2]
MOBIL = len(sys.argv) > 3 and sys.argv[3] == "mobil"
K = 2.4 if MOBIL else 1.0
els = json.load(open(src))["elements"]

LON0, LON1, LAT0, LAT1 = (10.9663, 10.9728, 49.4729, 49.4751) if MOBIL else (10.9655, 10.9740, 49.4727, 49.4752)
W = 1000
KX = 111320 * math.cos(math.radians((LAT0 + LAT1) / 2))
KY = 111320
SCALE = W / ((LON1 - LON0) * KX)
H = round((LAT1 - LAT0) * KY * SCALE)

def P(lat, lon):
    return ((lon - LON0) * KX * SCALE, (LAT1 - lat) * KY * SCALE)

def path(geom):
    return "M" + " L".join("%.1f,%.1f" % P(g["lat"], g["lon"]) for g in geom)

L = {k: [] for k in ["green", "allot", "bldg", "minor", "major", "rail", "wall", "open", "pipe", "basin"]}
BASIN = 1189199228            # unbenannter Graben in OSM = Lage des Betonbeckens (Luftbild DOP40)
for e in els:
    t, g = e.get("tags", {}), e.get("geometry")
    if e["type"] != "way" or not g:
        continue
    closed = g[0] == g[-1]
    if e["id"] == BASIN:
        L["basin"].append(path(g))
    elif "building" in t:
        L["bldg"].append(path(g) + "Z")
    elif t.get("landuse") == "allotments" and closed:
        L["allot"].append(path(g) + "Z")
    elif (t.get("landuse") in ("grass", "meadow") or t.get("natural") in ("scrub", "wood") or t.get("leisure") == "park") and closed:
        L["green"].append(path(g) + "Z")
    elif t.get("name") == "Scherbsgraben" and t.get("waterway"):
        L["pipe" if t.get("tunnel") else "open"].append(path(g))
    elif t.get("railway") == "rail":
        L["rail"].append(path(g))
    elif t.get("wall") == "noise_barrier":
        L["wall"].append(path(g))
    elif t.get("highway") in ("secondary", "tertiary"):
        L["major"].append(path(g))
    elif t.get("highway") in ("residential", "living_street", "unclassified"):
        L["minor"].append(path(g))

def grp(k, a):
    return f"<g {a}>" + "".join(f'<path d="{d}"/>' for d in L[k]) + "</g>"

F = "font-family=\"'Libre Franklin','Helvetica Neue',Arial,sans-serif\""
MARK = [  # Nr, lat, lon, Versatz der Marke (dx, dy) in px*K
    (1, 49.47342, 10.96691, (-14, -26) if not MOBIL else (4, -32)),   # Auslauf an der Breslauer Straße
    (2, 49.47367, 10.96754, (4, -28)),     # Übergang, verwildert (GPS Foto)
    (3, 49.47395, 10.97079, (0, -28)),     # Löwenkäfig (Einlauf, OSM)
    (4, 49.47445, 10.97100, (-28, -6)),    # Betonbecken an der Bahn
]
r = 13 * K
marks = ""
for n, la, lo, (dx, dy) in MARK:
    x, y = P(la, lo)
    mx, my = x + dx * K, y + dy * K
    marks += (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#121212" stroke-width="{1.2*K:.1f}"/>'
              f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3*K:.1f}" fill="#121212"/>'
              f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{r:.1f}" fill="#121212"/>'
              f'<text x="{mx:.1f}" y="{my+5*K:.1f}" {F} font-size="{14*K:.0f}" font-weight="700" fill="#fff" text-anchor="middle" style="stroke:none">{n}</text>')

def label(lat, lon, txt, size=13, color="#5a5a5a", anchor="middle", italic=False, weight=600, rot=0):
    x, y = P(lat, lon)
    tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
    st = ' font-style="italic"' if italic else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" {F} font-size="{size*K:.0f}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{st}{tr}>{txt}</text>'

labels = (
    label(49.47318, 10.96900, "RITTER-VON-ALDEBERT-STR." if not MOBIL else "R.-V.-ALDEBERT-STR.", 12, rot=-4)
    + (label(49.47395, 10.96660, "BRESLAUER STR.", 12, rot=-80) if not MOBIL else label(49.47470, 10.96700, "BRESLAUER STR.", 11, rot=-80))
    + label(49.47392, 10.96920, "Scherbsgraben", 14, "#3f6f95", italic=True, rot=-6)
    + (label(49.47290, 10.97000, "Bahn nach Würzburg", 12, "#121212", weight=400, rot=12) if not MOBIL else "")
    + (label(49.47470, 10.97180, "Bahn nach Bamberg", 12, "#121212", "start", weight=400, rot=-48) if not MOBIL else label(49.47372, 10.97200, "Bahn", 12, "#121212", "start", weight=400, rot=-48))
)

legend = "" if MOBIL else f'''<g {F} font-size="12" fill="#121212" transform="translate(12,12)">
  <rect width="214" height="62" fill="#fafaf8" fill-opacity="0.94" stroke="#dfdfdf"/>
  <line x1="10" y1="20" x2="40" y2="20" stroke="#7aa3c4" stroke-width="4"/><text x="50" y="24">offenes Bachbett (trocken)</text>
  <line x1="10" y1="44" x2="40" y2="44" stroke="#7aa3c4" stroke-width="3" stroke-dasharray="5 4"/><text x="50" y="48">im Rohr (verdolt)</text>
</g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="sg-t sg-d">
<title id="sg-t">Der Scherbsgraben an der Ritter-von-Aldebert-Straße</title>
<desc id="sg-d">Skizze: Der Scherbsgraben kommt verdolt unter Bahn und Breslauer Straße hindurch, tritt am Auslauf (1) zutage, verläuft knapp 300 Meter offen und trocken nördlich der Ritter-von-Aldebert-Straße, vorbei an einem verwilderten Übergang (2), und verschwindet am Löwenkäfig (3) wieder im Rohr Richtung Bamberger Bahn. Nördlich davon liegt an der Bahn ein Betonbecken (4).</desc>
<style>text{{paint-order:stroke;stroke:#fafaf8;stroke-width:{4*K:.0f}px;stroke-linejoin:round}}</style>
<rect width="{W}" height="{H}" fill="#fafaf8"/>
{grp("green", 'fill="#e3ecdc"')}
{grp("allot", 'fill="#eef2e8"')}
{grp("bldg", 'fill="#e2e2e0"')}
{grp("open", f'fill="none" stroke="#d5e5cc" stroke-width="{22*K:.0f}" stroke-linecap="round" stroke-linejoin="round"')}
{grp("minor", f'fill="none" stroke="#c4c4c0" stroke-width="{5*K:.1f}" stroke-linecap="round" stroke-linejoin="round"')}
{grp("major", f'fill="none" stroke="#8d8d8a" stroke-width="{9*K:.1f}" stroke-linecap="round" stroke-linejoin="round"')}
{grp("basin", f'fill="none" stroke="#9a9a96" stroke-width="{9*K:.1f}" stroke-linecap="butt"')}
{grp("wall", f'fill="none" stroke="#5a5a5a" stroke-width="{1.5*K:.1f}"')}
{grp("rail", f'fill="none" stroke="#121212" stroke-width="{3*K:.1f}"')}
{grp("rail", f'fill="none" stroke="#fafaf8" stroke-width="{1.6*K:.1f}" stroke-dasharray="8 8"')}
{grp("pipe", f'fill="none" stroke="#7aa3c4" stroke-width="{3*K:.1f}" stroke-dasharray="{5*K:.0f} {4*K:.0f}"')}
{grp("open", f'fill="none" stroke="#7aa3c4" stroke-width="{4*K:.1f}" stroke-linecap="round"')}
{labels}
{marks}
{legend}
<g transform="translate({W-24-100*SCALE:.1f},{H-26*K:.0f})" {F} font-size="{11*K:.0f}" fill="#121212">
  <line x1="0" y1="0" x2="{100*SCALE:.1f}" y2="0" stroke="#121212" stroke-width="{2*K:.0f}"/>
  <text x="{50*SCALE:.1f}" y="{16*K:.0f}" text-anchor="middle">100 m</text>
</g>
<text x="12" y="{H-10}" {F} font-size="{10*K:.0f}" fill="#5a5a5a">© OpenStreetMap-Mitwirkende</text>
</svg>'''
open(out, "w", encoding="utf-8").write(svg)
print("viewBox", W, H, "px/m", round(SCALE, 3), {k: len(v) for k, v in L.items()})
