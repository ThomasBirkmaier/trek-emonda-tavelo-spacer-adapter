"""
Adapter Trek Émonda SL 6 (2024) -> Tavelo Avro Rise
Parametrisches CadQuery-Modell. Maße in mm, Winkel in Grad.

Koordinatensystem (siehe 00_Anforderungen.md):
  Ursprung  = Schnittpunkt Schaftachse mit der Unterseite (Trek-Auflageebene)
  +x        = nach hinten (Richtung Oberrohr), -x = Fahrtrichtung
  y         = quer, Teil symmetrisch zu y = 0 (Teilungsebene)
  z         = Normale der Unterseite
  Schaftachse a = (sin aT, 0, cos aT): gegen z um ALPHA_TREK nach hinten geneigt.
  Oberseite: Tavelo-Ebene, Normale gegen die Achse um ALPHA_TAVELO geneigt (gleiche Richtung wie Trek).
  Keilwinkel zwischen Unter- und Oberseite = ALPHA_TREK - ALPHA_TAVELO (hinten dünn, vorn dick).
  Außenwand = Regelfläche zwischen Trek-Kontur (Unterseite) und Tavelo-Kontur (Oberseite), je in ihrer Ebene.
  Alles, was entlang des Schafts läuft oder geschoben wird (Außenwand, Bohrung, Sichel,
  Gelenk-Zapfen), ist entlang der Schaftachse extrudiert ("geschert").

Aufruf (aus dem Repo-Wurzelverzeichnis):  python 02_CAD/adapter.py
  -> 02_CAD/out/Adapter_H20_T<aT>_V<aV>.*      Adapter zusammengebaut (Ansicht/Kontrolle)
  -> 02_CAD/out/DRUCK_Adapter_...stl/.3mf/.step  Drucklayout, beide Hälften getrennt
  -> 02_CAD/out/DRUCK_Lehrkeil_<a>deg.*          Lehrkeile 15–19° zur Bestimmung von ALPHA_TREK
"""
import math
import os
import cadquery as cq

# ---------------------------------------------------------------- Parameter
# Winkel (ALPHA_TREK vorläufig, siehe 00_Anforderungen.md O-1)
ALPHA_TREK = 17.0         # Neigung Trek-Auflageebene gegen Schaftnormale -> Lehrkeile
ALPHA_TAVELO = 8.0        # gemessen 2026-09-28: Tavelo-Klemmbohrung 8° nach hinten gekippt bei flach aufliegender Sitzfläche

# Höhe
HEIGHT = 20.0             # Adapterhöhe entlang der Schaftachse (Durchstoßpunkt unten -> oben), wie ein Spacerstapel

# Schaft
STEERER_D = 28.6
STEERER_FLAT = 26.75      # seitliche Abflachungen (nur Info, Bohrung rund)
BORE_CLEAR = 0.15

# Außenkontur (Skizze V2; Freiform nach Vorgabe frei gestaltet)
REAR_X = 30.0
TIP_X = -28.0             # 13,0 ab vorderer Bohrungskante (bemaßt) + ~15
HALF_W = 19.75

# Trek-Nasen
NOSE_L, NOSE_W, NOSE_H = 7.6, 2.4, 1.5
NOSE_ANGLE = 24.0
NOSE_CX, NOSE_CY = 20.0, 7.9
POCKET_CLEAR = 0.3
POCKET_DEPTH = NOSE_H + 0.3

# Leitungskanal
CRESCENT_FRONT_X = TIP_X + 6.8
CRESCENT_HALF_OUT = 22.75 / 2
CRESCENT_HALF_IN = 20.2 / 2

# Stifte oben (greifen in die Sacklöcher der Tavelo-Vorbauunterseite)
PIN_D, PIN_H = 3.0, 1.85
PIN_X = REAR_X - 40.5
PIN_Y = 28.75 / 2

# Teilung + Gelenk nach Tavelo-Vorbild:
# An jeder Teilstelle greifen zwei Zapfen (Zylinder mit Hals) wechselseitig in Aufnahmen der anderen Hälfte:
# Hälfte A (y>0) trägt unten einen Zapfen, der in die Hälfte B ragt, Hälfte B trägt oben einen Zapfen, der in A ragt.
# Gefügt wird durch Aufschieben entlang des Schafts; die Zapfen sperren das Auseinanderziehen quer (y).
KERF = 0.25               # Fuge in der Teilungsebene
JOINT_CLEAR = 0.2         # radiales Spiel Zapfen/Aufnahme
JOINT_ZGAP = 0.15         # Luft in Schaftrichtung zwischen oberem und unterem Zapfen
JOINTS = [
    # x-Position, Zapfen-Ø, Versatz Zapfenmitte über die Fuge, Halsbreite
    # Versatz e > Zapfenradius + Spiel + ~0,6 mm, damit die Aufnahme echte Hinterschnitt-Lippen hat
    dict(x=-24.1, d=3.2, e=2.4, w=1.6),   # vorn, in der 6,8-mm-Wand vor der Sichel
    dict(x=26.0, d=4.0, e=2.9, w=2.2),    # hinten, zwischen den Nasen
]

# Lehrkeile
GAUGE_T = 4.0
GAUGE_ANGLES = [15.0, 16.0, 17.0, 18.0, 19.0]

BIG = 200.0


# ---------------------------------------------------------------- Hilfsfunktionen
def outline_wire_pts():
    up = [
        (TIP_X, 0.0), (-26.6, 5.0), (-23.4, 10.0), (-18.6, 14.6), (-12.8, 17.9),
        (-6.0, 19.4), (0.0, HALF_W), (8.0, 19.4), (17.0, 16.8), (23.0, 14.7),
        (26.8, 12.6), (28.9, 9.4), (29.8, 5.0), (REAR_X, 0.0),
    ]
    return up + [(x, -y) for (x, y) in reversed(up[1:-1])]


def _wire(pts, z, dx, spline, periodic=True):
    wp = cq.Workplane("XY").workplane(offset=z)
    p = [(x + dx, y) for x, y in pts]
    if spline:
        wp = wp.spline(p, periodic=periodic, includeCurrent=False) if periodic else wp.spline(p, includeCurrent=False).close()
        if periodic:
            wp = wp.close()
    else:
        wp = wp.polyline(p).close()
    return wp.wire().val()


def axial_prism(pts, alpha, z0, z1, spline=False, periodic=True):
    """Profil (in Ebene parallel zur Unterseite) entlang der Schaftachse von z0 bis z1 extrudiert."""
    t = math.tan(math.radians(alpha))
    return cq.Workplane("XY").add(cq.Solid.makeLoft(
        [_wire(pts, z0, z0 * t, spline, periodic), _wire(pts, z1, z1 * t, spline, periodic)], True))


def axial_cylinder(cx, cy, r, alpha, z0, z1):
    t = math.tan(math.radians(alpha))
    c0 = cq.Workplane("XY").workplane(offset=z0).center(cx + z0 * t, cy).circle(r).wire().val()
    c1 = cq.Workplane("XY").workplane(offset=z1).center(cx + z1 * t, cy).circle(r).wire().val()
    return cq.Workplane("XY").add(cq.Solid.makeLoft([c0, c1], True))


def box_between(xa, xb, ya, yb, za, zb):
    return cq.Workplane("XY").box(xb - xa, yb - ya, zb - za, centered=False).translate((xa, ya, za))


def top_frame(aT, aV, h):
    """Punkt P (Achse ∩ Oberseite, h entlang der Achse), Normale n und x-Richtung u der Oberseite."""
    tT = math.radians(aT)
    P = cq.Vector(h * math.sin(tT), 0, h * math.cos(tT))
    d = math.radians(aT - aV)          # Neigung der Oberseiten-Normale gegen z
    n = cq.Vector(math.sin(d), 0, math.cos(d))
    u = cq.Vector(math.cos(d), 0, -math.sin(d))
    return P, n, u, d


def above_top_cutter(aT, aV, h):
    P, n, u, d = top_frame(aT, aV, h)
    return (box_between(-BIG / 2, BIG / 2, -BIG / 2, BIG / 2, 0, BIG)
            .rotate((0, 0, 0), (0, 1, 0), math.degrees(d)).translate(P))


# ---------------------------------------------------------------- Features
def envelope(aT, aV, h):
    """Regelfläche zwischen Trek-Kontur in der Unterseite (z=0) und Tavelo-Kontur in der Oberseite.
    Beide Konturen sind relativ zum jeweiligen Durchstoßpunkt der Schaftachse definiert."""
    P, n, u, d = top_frame(aT, aV, h)
    pts = outline_wire_pts()
    bottom = cq.Workplane("XY").spline(pts, periodic=True, includeCurrent=False).close().wire().val()
    top = (cq.Workplane("XY").spline(pts, periodic=True, includeCurrent=False).close()
           .rotate((0, 0, 0), (0, 1, 0), math.degrees(d)).translate(P).wire().val())
    return cq.Workplane("XY").add(cq.Solid.makeLoft([bottom, top], True))


def bore_cutter(aT):
    return axial_cylinder(0, 0, STEERER_D / 2 + BORE_CLEAR, aT, -20, 60)


def crescent_cutter(aT):
    up = [(-10.5, CRESCENT_HALF_IN), (-13.5, CRESCENT_HALF_IN + 0.35), (-16.5, CRESCENT_HALF_IN + 0.8),
          (-18.9, CRESCENT_HALF_OUT), (-20.5, 9.6), (-21.1, 7.0), (CRESCENT_FRONT_X, 3.5)]
    pts = up + [(CRESCENT_FRONT_X, 0.0)] + [(x, -y) for (x, y) in reversed(up)]
    return axial_prism(pts, aT, -20, 60, spline=True, periodic=False)


def nose_pocket_cutters():
    L, W = NOSE_L + 2 * POCKET_CLEAR, NOSE_W + 2 * POCKET_CLEAR
    res = None
    for s in (1, -1):
        ang = 180.0 - NOSE_ANGLE if s == 1 else 180.0 + NOSE_ANGLE
        p = (cq.Workplane("XY").workplane(offset=-1.0)
             .center(NOSE_CX, s * NOSE_CY).slot2D(L, W, ang).extrude(POCKET_DEPTH + 1.0))
        res = p if res is None else res.union(p)
    return res


def pins(aT, aV, h):
    """Stifte senkrecht auf der Tavelo-Ebene, Lage in Oberseiten-Koordinaten relativ zum Achsdurchstoßpunkt."""
    P, n, u, d = top_frame(aT, aV, h)
    res = None
    for s in (1, -1):
        c = P + u * PIN_X + cq.Vector(0, s * PIN_Y, 0)
        pin = (cq.Workplane("XY").circle(PIN_D / 2).extrude(PIN_H + 0.6).translate((0, 0, -0.6))
               .rotate((0, 0, 0), (0, 1, 0), math.degrees(d)).translate(c))
        res = pin if res is None else res.union(pin)
    return res


def knuckle(j, side, aT, z0, z1, grow=0.0):
    """Zapfen (Zylinder + Hals). side=+1: gehört zu A (y>0), ragt nach -y; side=-1: gehört zu B, ragt nach +y.
    grow>0 erzeugt die Aufnahme (mit Spiel) statt des Zapfens."""
    cy = -side * j["e"]
    r = j["d"] / 2 + grow
    hw = j["w"] / 2 + grow
    cyl = axial_cylinder(j["x"], cy, r, aT, z0, z1)
    y_from = side * (KERF / 2 + 1.0)          # Hals beginnt im eigenen Körper
    neck = axial_prism([(j["x"] - hw, min(y_from, cy)), (j["x"] + hw, min(y_from, cy)),
                        (j["x"] + hw, max(y_from, cy)), (j["x"] - hw, max(y_from, cy))], aT, z0, z1)
    return cyl.union(neck)


def split_halves(body, aT, h, with_joints=True):
    A = body.intersect(box_between(-BIG / 2, BIG / 2, KERF / 2, BIG / 2, -BIG / 2, BIG / 2))
    B = body.intersect(box_between(-BIG / 2, BIG / 2, -BIG / 2, -KERF / 2, -BIG / 2, BIG / 2))
    if not with_joints:
        return A, B
    zm = h * math.cos(math.radians(aT)) / 2      # Teilungshöhe der Zapfen: halbe Höhe an der Achse
    for j in JOINTS:
        # A: unterer Zapfen nach B, Aufnahme oben für den Zapfen von B
        kA = knuckle(j, +1, aT, 0.0, zm - JOINT_ZGAP).intersect(body)
        sA = knuckle(j, -1, aT, zm - JOINT_ZGAP, h + 20, grow=JOINT_CLEAR)
        # B: oberer Zapfen nach A, Aufnahme unten für den Zapfen von A
        kB = knuckle(j, -1, aT, zm + JOINT_ZGAP, h + 20).intersect(body)
        sB = knuckle(j, +1, aT, -20, zm + JOINT_ZGAP, grow=JOINT_CLEAR)
        A = A.cut(sA).union(kA)
        B = B.cut(sB).union(kB)
    return A, B


# ---------------------------------------------------------------- Bauteile
def adapter(aT=ALPHA_TREK, aV=ALPHA_TAVELO, h=HEIGHT, label=None, with_joints=True):
    body = envelope(aT, aV, h).union(pins(aT, aV, h))
    if label:
        P, n, u, d = top_frame(aT, aV, h)
        c = P + u * 9.0 + cq.Vector(0, -16.2, 0)
        txt = (cq.Workplane("XY").text(label, 4.0, 1.2, kind="bold", halign="center", valign="center")
               .translate((0, 0, -0.6)).rotate((0, 0, 0), (0, 1, 0), math.degrees(d)).translate(c))
        body = body.cut(txt)
    A, B = split_halves(body, aT, h, with_joints)
    holes = bore_cutter(aT).union(crescent_cutter(aT)).union(nose_pocket_cutters())
    A, B = A.cut(holes), B.cut(holes)
    return A, B


def gauge(alpha):
    """Lehrkeil: Adaptergeometrie in 4 mm, Ober- und Unterseite parallel (nur Trek-Seite wird geprüft).
    Zweiteilig ohne Gelenk – die Hälften werden beim Prüfen von Hand gehalten."""
    return adapter(alpha, alpha, GAUGE_T / math.cos(math.radians(alpha)), label=f"{alpha:g}", with_joints=False)


def export_pair(A, B, path_stem):
    both = cq.Workplane("XY").add(A.vals()).add(B.vals())
    cq.exporters.export(both, path_stem + ".step")
    cq.exporters.export(both, path_stem + ".stl", tolerance=0.02, angularTolerance=0.1)
    return sum(v.Volume() for v in A.solids().vals()) + sum(v.Volume() for v in B.solids().vals())


def export_print_layout(A, B, path_stem, gap=8.0):
    """Drucklayout: beide Hälften in einer Datei, aber auseinandergezogen (nicht verschränkt),
    Unterseite (Trek-Auflage) auf z = 0. Abstand so, dass sich die übergreifenden Zapfen nicht berühren."""
    a = A.translate((0, gap, 0))
    b = B.translate((0, -gap, 0))
    both = cq.Workplane("XY").add(a.vals()).add(b.vals())
    inter = a.intersect(b).solids().vals()
    assert not inter, "Hälften berühren sich im Drucklayout"
    cq.exporters.export(both, path_stem + ".stl", tolerance=0.01, angularTolerance=0.08)
    cq.exporters.export(both, path_stem + ".step")
    cq.exporters.export(both, path_stem + ".3mf", tolerance=0.01, angularTolerance=0.08)
    bb = both.val().BoundingBox() if len(both.vals()) == 1 else cq.Compound.makeCompound(both.vals()).BoundingBox()
    return bb


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out, exist_ok=True)
    A, B = adapter()
    v = export_pair(A, B, os.path.join(out, f"Adapter_H{HEIGHT:g}_T{ALPHA_TREK:g}_V{ALPHA_TAVELO:g}"))
    print("Adapter", "Körper A/B:", len(A.solids().vals()), len(B.solids().vals()), "Volumen %.0f mm3" % v)
    bb = export_print_layout(A, B, os.path.join(out, f"DRUCK_Adapter_H{HEIGHT:g}_T{ALPHA_TREK:g}_V{ALPHA_TAVELO:g}"))
    print("  Drucklayout Bauraum %.1f x %.1f x %.1f mm" % (bb.xlen, bb.ylen, bb.zlen))
    for a in GAUGE_ANGLES:
        A, B = gauge(a)
        name = f"Lehrkeil_{a:04.1f}deg".replace(".", "_")
        export_print_layout(A, B, os.path.join(out, "DRUCK_" + name), gap=3.0)
        print(name)
