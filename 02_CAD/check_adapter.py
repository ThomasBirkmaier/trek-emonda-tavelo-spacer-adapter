"""Prüfungen nach jeder Geometrieänderung: Körper, Kollision der Hälften, Bohrungsmaß, Wandstärken.
Beide Varianten (adapter.VARIANTS) werden geprüft; sie unterscheiden sich nur an den Stiften oben.

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
pin_holes = A.pin_holes(aT, aV, h).intersect(env).val()
core = A.core_body(aT, aV, h)
holes = env.cut(core).val()   # Bohrung + Kanal inkl. Kantenradien
hose = A.hose_cutters(aT)


def wall_out(solid):
    return min(solid.distance(f) for f in side)


failed = False
for var in A.VARIANTS:
    a, b = A.adapter(variant=var, core=core)
    inter = sum(s.Volume() for s in a.intersect(b).solids().vals())
    vol = sum(s.Volume() for s in a.solids().vals()) + sum(s.Volume() for s in b.solids().vals())
    print(f"Variante {var:10s} Körper A/B: {len(a.solids().vals())}/{len(b.solids().vals())}"
          f"   Volumen {vol:.0f} mm³   A∩B {inter:.3f} mm³")
    failed |= inter > 1e-6

# Bohrung senkrecht zur Achse
loc = bore.rotate(cq.Vector(), cq.Vector(0, 1, 0), -aT).BoundingBox()
print(f"Bohrung senkrecht zur Achse: längs {loc.xmin:.2f} … {loc.xmax:.2f} ({loc.xlen:.2f}), quer {loc.ylen:.2f}"
      f"   Schaft Ø {A.STEERER_D}")
print(f"Passstift: Ø 3 × {A.DOWEL_L:g}, Überstand {A.PIN_H:g}, im Loch {A.DOWEL_L - A.PIN_H:.2f};"
      f" Sackloch Ø {A.PINHOLE_D:g} × {A.PINHOLE_DEPTH:.2f}, Fase {A.PINHOLE_CHAMFER:g}")

# Wandstärken
rows = []
print(f"Nasentaschen zur Bohrung {'offen' if bore.distance(pockets) < 1e-6 else 'GESCHLOSSEN'}")
rows.append(("Stift ↔ Bohrung/Kanal (Variante Stift)", pins.distance(holes)))
rows.append(("Stift ↔ Außenwand (Variante Stift)", wall_out(pins)))
rows.append(("Sackloch ↔ Bohrung/Kanal (Variante Passstift)", pin_holes.distance(holes)))
rows.append(("Sackloch ↔ Außenwand (Variante Passstift)", wall_out(pin_holes)))
if hose is not None:
    rows.append(("Sackloch ↔ Leitungsschräge (Variante Passstift)", pin_holes.distance(hose.val())))
rows.append(("Bohrung ↔ Außenwand", wall_out(bore)))
if hose is not None:
    rows.append(("Leitungsschräge ↔ Außenwand", wall_out(hose.intersect(env).val())))
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
    print(f"  {'!' if d < MIN_WALL else ' '} {name:52s} {d:6.2f}")
if failed:
    sys.exit("FEHLER: Hälften überschneiden sich")
