"""Erzeugt die Lageskizze Ritter-von-Aldebert-Straße als SVG aus OSM-Daten (geo.json).
Aufruf: python3 -I scripts/make_lageskizze.py geo.json out.svg [mobil]
Desktop: assets/img/ritter-aldebert/lageskizze.svg · Mobil: lageskizze-mobil.svg
"""
import json, math, sys

src, out = sys.argv[1], sys.argv[2]
MOBIL = len(sys.argv) > 3 and sys.argv[3] == "mobil"
K = 1.0 if not MOBIL else 2.3   # Schrift-/Abstandsfaktor
els = json.load(open(src))["elements"]

LON0, LON1, LAT0, LAT1 = (10.9640, 10.9745, 49.4716, 49.4752) if not MOBIL else (10.9652, 10.9732, 49.4719, 49.4750)
W = 1000
KX = 111320 * math.cos(math.radians((LAT0 + LAT1) / 2))
KY = 111320
SCALE = W / ((LON1 - LON0) * KX)          # px pro Meter
H = round((LAT1 - LAT0) * KY * SCALE)

def P(lat, lon):
    return ((lon - LON0) * KX * SCALE, (LAT1 - lat) * KY * SCALE)

def path(geom, close=False):
    pts = [P(g["lat"], g["lon"]) for g in geom]
    s = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return s + ("Z" if close else "")

def inside(lat, lon, poly):
    c = False
    for i in range(len(poly)):
        (y1, x1), (y2, x2) = poly[i], poly[i - 1]
        if (y1 > lat) != (y2 > lat) and lon < (x2 - x1) * (lat - y1) / (y2 - y1) + x1:
            c = not c
    return c

# Geltungsbereich, schematisch nach Plan Stadtplanungsamt 28.04.2026 (lat, lon)
GB = [(49.47343, 10.96690), (49.47398, 10.97079), (49.47420, 10.97222), (49.47392, 10.97255),
      (49.47333, 10.97200), (49.47322, 10.97130), (49.47318, 10.97070), (49.47326, 10.96900),
      (49.47334, 10.96700)]

# Geltungsbereich Bebauungsplan Nr. 256 – schematisch nach dem Plan von 1973:
# zwischen Bahnlinie Nürnberg–Würzburg (Süden), Nürnberg–Bamberg (Osten) und Cadolzburger Straße (Norden)
BP256 = [(49.47378, 10.9630), (49.47391, 10.96407), (49.47402, 10.96627), (49.47444, 10.96651),
         (49.47462, 10.96800), (49.47494, 10.97008), (49.47505, 10.97050), (49.47407, 10.97154),
         (49.47228, 10.97484), (49.47188, 10.97230), (49.47310, 10.96618), (49.47320, 10.96569),
         (49.47350, 10.96420), (49.47362, 10.9630)]
# Grenze Volkswohl (West/Mitte) / WBG Nr. 51/53 (Osten) – schematisch
DIV = [(49.47321, 10.97110), (49.47403, 10.97110)]

# Mittlere, nicht sanierte Volkswohl-Blöcke – vermutlich Abriss (Ortsbesichtigung 06.11.2026)
ABRISS = {204357446, 204357447}

layers = {k: [] for k in ["green", "water", "bldg", "bldg_gb", "bldg_abr", "minor", "major", "rail", "path", "rva"]}
bus = []
for e in els:
    t = e.get("tags", {})
    if e["type"] == "node":
        if t.get("highway") == "bus_stop" and "Aldebert" in t.get("name", ""):
            bus.append(P(e["lat"], e["lon"]))
        continue
    g = e.get("geometry")
    if not g:
        continue
    closed = g[0] == g[-1]
    if "building" in t:
        c = (sum(p["lat"] for p in g) / len(g), sum(p["lon"] for p in g) / len(g))
        key = "bldg_abr" if e["id"] in ABRISS else ("bldg_gb" if inside(c[0], c[1], GB) else "bldg")
        layers[key].append(path(g, True))
    elif t.get("landuse") in ("grass", "meadow") or t.get("natural") in ("scrub", "wood") or t.get("leisure") == "park":
        if closed:
            layers["green"].append(path(g, True))
    elif t.get("waterway") and t.get("name") == "Scherbsgraben" and t.get("tunnel") is None:
        layers["water"].append(path(g))
    elif t.get("railway") == "rail":
        layers["rail"].append(path(g))
    elif "Aldebert" in t.get("name", "") and t.get("highway") == "residential":
        layers["rva"].append(path(g))
    elif "Aldebert" in t.get("name", "") and t.get("highway") == "path":
        layers["path"].append(path(g))
    elif t.get("highway") in ("secondary", "tertiary"):
        layers["major"].append(path(g))
    elif t.get("highway") in ("residential", "living_street", "unclassified"):
        layers["minor"].append(path(g))

def grp(key, attrs):
    return f'<g {attrs}>' + "".join(f'<path d="{d}"/>' for d in layers[key]) + "</g>"

jx, jy = P(49.47345, 10.96621)          # Einmündung Breslauer Str.
ex, ey = P(49.47331, 10.97134)          # Ende Fahrbahn
gbx, gby = P(49.47372, 10.96980)
brx, bry = P(49.47312, 10.96590)        # Bahnbrücke
grx, gry = P(49.47405, 10.96880)
vwx, vwy = P(49.47347, 10.96830)        # Label Volkswohl
wbx, wby = P(49.47368, 10.97180)        # Label WBG

F = "font-family=\"'Libre Franklin','Helvetica Neue',Arial,sans-serif\""
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="lage-t lage-d">
<title id="lage-t">Lageskizze Ritter-von-Aldebert-Straße</title>
<desc id="lage-d">Die Ritter-von-Aldebert-Straße zweigt als einzige Zufahrt von der Breslauer Straße direkt neben der Bahnbrücke ab und endet für Autos nach rund 380 Metern als Sackgasse. Nördlich davon liegt zwischen Straße und Scherbsgraben der Änderungsbereich für rund 130 neue Wohnungen (Volkswohl im Westen und in der Mitte, WBG Nr. 51/53 im Osten). Die Grenze des geltenden Bebauungsplans Nr. 256 ist schematisch eingezeichnet.</desc>
<style>text{{paint-order:stroke;stroke:#fafaf8;stroke-width:{4*K:.0f}px;stroke-linejoin:round}}</style>
<rect width="{W}" height="{H}" fill="#fafaf8"/>
{grp("green", 'fill="#e3ecdc"')}
{grp("water", 'fill="none" stroke="#e3ecdc" stroke-width="26" stroke-linecap="round"')}
{grp("water", 'fill="none" stroke="#7aa3c4" stroke-width="2"')}
{grp("bldg", 'fill="#e2e2e0"')}
<path d="{path([{"lat": a, "lon": b} for a, b in GB], True)}" fill="#a8442a" fill-opacity="0.12" stroke="#a8442a" stroke-width="2" stroke-dasharray="7 5"/>
{grp("bldg_gb", 'fill="#9a9a96"')}
<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#f3e3dd"/><line x1="0" y1="0" x2="0" y2="6" stroke="#a8442a" stroke-width="2.5"/></pattern></defs>
{grp("bldg_abr", 'fill="url(#hatch)" stroke="#a8442a" stroke-width="1.5"')}
<path d="{path([{"lat": a, "lon": b} for a, b in DIV])}" fill="none" stroke="#a8442a" stroke-width="{1.5*K:.1f}" stroke-dasharray="4 4"/>
{grp("minor", 'fill="none" stroke="#c4c4c0" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"')}
{grp("major", 'fill="none" stroke="#8d8d8a" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"')}
{grp("rail", 'fill="none" stroke="#121212" stroke-width="3"')}
{grp("rail", 'fill="none" stroke="#fafaf8" stroke-width="1.6" stroke-dasharray="8 8"')}
<path d="{path([{"lat": a, "lon": b} for a, b in BP256], True)}" fill="none" stroke="#fafaf8" stroke-width="{5*K:.1f}" stroke-opacity="0.8"/>
<path d="{path([{"lat": a, "lon": b} for a, b in BP256], True)}" fill="none" stroke="#3d3d3a" stroke-width="{2.2*K:.1f}" stroke-dasharray="14 5 3 5"/>
{grp("path", 'fill="none" stroke="#121212" stroke-width="2" stroke-dasharray="3 4"')}
{grp("rva", 'fill="none" stroke="#121212" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"')}
''' + "".join(f'<rect x="{x-6*K:.1f}" y="{y-6*K:.1f}" width="12" height="12" fill="#326891"/><text x="{x+9*K:.1f}" y="{y+4*K:.1f}" {F} font-size="{13*K:.0f}" font-weight="600" fill="#326891">H</text>' for x, y in bus) + f'''
''' + (f'''<circle cx="{jx:.1f}" cy="{jy:.1f}" r="22" fill="none" stroke="#a8442a" stroke-width="4"/>
<g {F} fill="#121212">
  <text x="{jx+34:.1f}" y="{jy-180:.1f}" font-size="40" font-weight="600">Einzige Zufahrt</text>
  <path d="M{jx+60:.1f},{jy-168:.1f} L{jx+12:.1f},{jy-22:.1f}" stroke="#121212" stroke-width="2"/>
  <text x="{gbx+40:.1f}" y="{gby-40:.1f}" font-size="38" font-weight="600" fill="#a8442a" text-anchor="middle">Änderungsbereich</text>
  <text x="{gbx+40:.1f}" y="{gby+2:.1f}" font-size="30" fill="#a8442a" text-anchor="middle">≈ 130 Wohnungen + KiTa</text>
  <text x="{(jx+ex)/2:.1f}" y="{(jy+ey)/2+78:.1f}" font-size="32" font-weight="600" text-anchor="middle">RITTER-V.-ALDEBERT-STR.</text>
  <text x="{W-16}" y="{ey+150:.1f}" font-size="38" font-weight="600" text-anchor="end">Sackgasse</text>
  <path d="M{ex+20:.1f},{ey+112:.1f} L{ex:.1f},{ey+14:.1f}" stroke="#121212" stroke-width="2"/>
  <text x="64" y="{H-24}" font-size="28" font-weight="600" fill="#5a5a5a">Breslauer Str.</text>
  <text x="{vwx:.1f}" y="{vwy+4:.1f}" font-size="26" font-weight="600" fill="#a8442a" text-anchor="middle">Volkswohl</text>
  <text x="{wbx:.1f}" y="{wby+4:.1f}" font-size="26" font-weight="600" fill="#a8442a" text-anchor="middle">WBG</text>
</g>
<g {F} font-size="30" fill="#121212" transform="translate({W-412},10)">
  <rect x="0" y="0" width="402" height="156" fill="#fafaf8" fill-opacity="0.94" stroke="#dfdfdf"/>
  <rect x="12" y="16" width="38" height="26" fill="#a8442a" fill-opacity="0.12" stroke="#a8442a" stroke-width="2" stroke-dasharray="5 4"/>
  <text x="62" y="40">Änderungsbereich</text>
  <rect x="17" y="62" width="28" height="24" fill="url(#hatch)" stroke="#a8442a" stroke-width="2"/>
  <text x="62" y="84">vermutlich Abriss</text>
  <line x1="10" y1="124" x2="52" y2="124" stroke="#3d3d3a" stroke-width="3.5" stroke-dasharray="14 5 3 5"/>
  <text x="62" y="134">B-Plan Nr. 256</text>
</g>
<g {F} font-size="24" fill="#5a5a5a"><text x="{W-12}" y="{H-14}" text-anchor="end">© OpenStreetMap-Mitwirkende</text></g>
''' if MOBIL else f'''<circle cx="{jx:.1f}" cy="{jy:.1f}" r="15" fill="none" stroke="#a8442a" stroke-width="3"/>
<g {F} fill="#121212">
  <text x="{jx-22*K:.1f}" y="{jy-40*K:.1f}" font-size="{16*K:.0f}" font-weight="600" text-anchor="end">Einzige Zufahrt</text>
  {"" if MOBIL else f'<text x="{jx-22*K:.1f}" y="{jy-22*K:.1f}" font-size="{13*K:.0f}" fill="#5a5a5a" text-anchor="end">an der Breslauer Straße</text>'}
  <path d="M{jx-20*K:.1f},{jy-18*K:.1f} L{jx-10*K:.1f},{jy-10*K:.1f}" stroke="#121212" stroke-width="1"/>
  <text x="{ex-20*K:.1f}" y="{ey+62*K:.1f}" font-size="{16*K:.0f}" font-weight="600">Sackgasse für Autos</text>
  {"" if MOBIL else f'<text x="{ex-20*K:.1f}" y="{ey+80*K:.1f}" font-size="{13*K:.0f}" fill="#5a5a5a">weiter nur Fuß- und Radweg</text>'}
  <path d="M{ex-10*K:.1f},{ey+46*K:.1f} L{ex:.1f},{ey+8*K:.1f}" stroke="#121212" stroke-width="1"/>
  <text x="{gbx:.1f}" y="{gby-34*K:.1f}" font-size="{17*K:.0f}" font-weight="600" fill="#a8442a" text-anchor="middle">Änderungsbereich</text>
  <text x="{gbx:.1f}" y="{gby-16*K:.1f}" font-size="{13*K:.0f}" fill="#a8442a" text-anchor="middle">{"≈ 130 Wohnungen + KiTa" if MOBIL else "ca. 130 neue Wohnungen + KiTa"}</text>
  <text x="{(jx+ex)/2+40*K:.1f}" y="{(jy+ey)/2+52*K:.1f}" font-size="{14*K:.0f}" font-weight="600" text-anchor="middle" letter-spacing="0.5">{"RITTER-VON-ALDEBERT-STR." if MOBIL else "RITTER-VON-ALDEBERT-STRASSE · ca. 380 m"}</text>
  <text x="{brx-22*K:.1f}" y="{bry+30*K:.1f}" font-size="{13*K:.0f}" fill="#5a5a5a" text-anchor="end">Bahnbrücke</text>
  <text x="{grx:.1f}" y="{gry-22*K:.1f}" font-size="{13*K:.0f}" fill="#5b7f4f" text-anchor="middle" font-style="italic">{"Scherbsgraben" if MOBIL else "Grünzug Scherbsgraben"}</text>
  <text x="{P(49.47265,10.96535)[0]+16:.1f}" y="{P(49.47265,10.96535)[1]+4:.1f}" font-size="{13*K:.0f}" font-weight="600" fill="#5a5a5a" letter-spacing="0.5">BRESLAUER STRASSE</text>
  <text x="{vwx:.1f}" y="{vwy:.1f}" font-size="12" font-weight="600" fill="#a8442a" text-anchor="middle">Volkswohl</text>
  <text x="{wbx:.1f}" y="{wby:.1f}" font-size="12" font-weight="600" fill="#a8442a" text-anchor="middle">WBG</text>
  <text x="{wbx:.1f}" y="{wby+14:.1f}" font-size="11" fill="#a8442a" text-anchor="middle">Nr. 51/53</text>
</g>
<g {F} font-size="12" fill="#121212" transform="translate({W-318},12)">
  <rect x="0" y="0" width="306" height="104" fill="#fafaf8" fill-opacity="0.94" stroke="#dfdfdf"/>
  <rect x="10" y="10" width="22" height="14" fill="#a8442a" fill-opacity="0.12" stroke="#a8442a" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text x="40" y="22">Änderungsbereich 3. Änderung (Stand 28.04.2026)</text>
  <rect x="13" y="34" width="16" height="12" fill="#9a9a96"/>
  <text x="40" y="45">Bestand, saniert bzw. bleibt</text>
  <rect x="13" y="54" width="16" height="12" fill="url(#hatch)" stroke="#a8442a"/>
  <text x="40" y="65">vermutlich Abriss (Ortsbesichtigung)</text>
  <line x1="8" y1="84" x2="34" y2="84" stroke="#3d3d3a" stroke-width="2.2" stroke-dasharray="14 5 3 5"/>
  <text x="40" y="88">Geltungsbereich B-Plan Nr. 256 (schematisch)</text>
</g>
<g {F} font-size="{12*K:.0f}" fill="#5a5a5a">
  <rect x="{W-(560 if not MOBIL else 420)}" y="{H-30*K:.0f}" width="{560 if not MOBIL else 420}" height="{30*K:.0f}" fill="#fafaf8" fill-opacity="0.9"/>
  <text x="{W-12}" y="{H-11*K:.0f}" text-anchor="end">{"© OpenStreetMap-Mitwirkende" if MOBIL else "Kartengrundlage © OpenStreetMap-Mitwirkende (ODbL) · Grenzen schematisch"}</text>
</g>
<g transform="translate(24,{H-80*K:.0f})" {F} font-size="{12*K:.0f}" fill="#121212">
  <line x1="0" y1="10" x2="{100*SCALE:.1f}" y2="10" stroke="#121212" stroke-width="2"/>
  <text x="0" y="28">0</text><text x="{100*SCALE:.1f}" y="28" text-anchor="middle">100 m</text>
  <path d="M0,-30 l6,14 l-6,-4 l-6,4z" transform="translate(140,10)" fill="#121212"/><text x="140" y="-34" text-anchor="middle">N</text>
</g>
''') + '''</svg>'''
open(out, "w", encoding="utf-8").write(svg)
print("viewBox", W, H, "scale px/m", round(SCALE, 3), "bus", len(bus))
