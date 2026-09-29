"""Prüfungen nach jeder Geometrieänderung: Körper, Kollision der Hälften, Bohrungsmaß, Wandstärken.

Aufruf (aus dem Repo-Wurzelverzeichnis):  python 02_CAD/check_adapter.py
Wandstärken sind kürzeste Abstände zwischen den Schnittkörpern (OCCT), in mm.
Die Nasentaschen sind absichtlich zur Bohrung geöffnet (POCKET_BRIDGE), dort ist der Abstand 0.
"""
import math
import sys

sys.path.insert(0, "02_CAD")
import adapter as A  # noqa: E402
import cadquery as cq  # noqa: E402

MIN_WALL = 1.2   # Warnschwelle

aT, aV, h = A.ALPHA_TREK, A.ALPHA_TAVELO, A.HEIGHT
env = A.envelope(aT, aV, h)
side = [f for f in env.val().Faces() if f.geomType() != "PLANE"]   # Außenwand ohne Ober-/Unterseite
bore = A.bore_cutter(aT).val()
pockets = A.nose_pocket_cutters(aT).val()
pins = A.pins(aT, aV, h).val()
holes = env.cut(A.core_body(aT, aV, h)).val()   # Bohrung + Kanal inkl. Kantenradien


def wall_out(solid):
    return min(solid.distance(f) for f in side)


rows = []
# Hälften
a, b = A.adapter()
inter = sum(s.Volume() for s in a.intersect(b).solids().vals())
vol = sum(s.Volume() for s in a.solids().vals()) + sum(s.Volume() for s in b.solids().vals())
print(f"Körper A/B: {len(a.solids().vals())}/{len(b.solids().vals())}   Volumen {vol:.0f} mm³   A∩B {inter:.3f} mm³")

# Bohrung senkrecht zur Achse
loc = bore.rotate(cq.Vector(), cq.Vector(0, 1, 0), -aT).BoundingBox()
print(f"Bohrung senkrecht zur Achse: längs {loc.xmin:.2f} … {loc.xmax:.2f} ({loc.xlen:.2f}), quer {loc.ylen:.2f}"
      f"   Schaft Ø {A.STEERER_D}")

# Wandstärken
print(f"Nasentaschen zur Bohrung {'offen' if bore.distance(pockets) < 1e-6 else 'GESCHLOSSEN'}")
rows.append(("Bohrung ↔ Stift", bore.distance(pins)))   # Wand; die Bohrungsrundung (R1) liegt auf der Oberseite dazwischen
rows.append(("Bohrung ↔ Außenwand", wall_out(bore)))
rows.append(("Stift ↔ Außenwand", wall_out(pins)))
zm = h * math.cos(math.radians(aT)) / 2
for j in A.JOINTS:
    tag = "vorn" if j["x"] < 0 else "hinten"
    for name, (s, z0, z1) in {"unten": (+1, -20, zm + A.JOINT_ZGAP), "oben": (-1, zm - A.JOINT_ZGAP, h + 20)}.items():
        r = A.knuckle(j, s, aT, z0, z1, grow=A.JOINT_CLEAR).intersect(env).val()
        rows.append((f"Gelenk {tag} {name} (x={j['x']}) ↔ Bohrung/Kanal", r.distance(holes)))
        rows.append((f"Gelenk {tag} {name} (x={j['x']}) ↔ Außenwand", wall_out(r)))
        if j["x"] > 0:   # nur das hintere Gelenk liegt neben den Nasentaschen
            rows.append((f"Gelenk {tag} {name} (x={j['x']}) ↔ Nasentasche", r.distance(pockets)))

print("\nWandstärken:")
for name, d in rows:
    print(f"  {'!' if d < MIN_WALL else ' '} {name:48s} {d:6.2f}")
if inter > 1e-6:
    sys.exit("FEHLER: Hälften überschneiden sich")
