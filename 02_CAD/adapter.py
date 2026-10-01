"""
Adapter Trek Émonda SL 6 (2024) -> Tavelo Avro Rise
Parametrisches CadQuery-Modell. Maße in mm, Winkel in Grad.

Koordinatensystem (siehe KONSTRUKTION.md):
  Ursprung  = Schnittpunkt Schaftachse mit der Unterseite (Trek-Auflageebene)
  +x        = nach hinten (Richtung Oberrohr), -x = Fahrtrichtung
  y         = quer, Teil symmetrisch zu y = 0 (Teilungsebene)
  z         = Normale der Unterseite
  Schaftachse a = (sin aT, 0, cos aT): gegen z um ALPHA_TREK nach hinten geneigt.
  Oberseite: Tavelo-Ebene, Normale gegen die Achse um ALPHA_TAVELO geneigt (gleiche Richtung wie Trek).
  Keilwinkel zwischen Unter- und Oberseite = ALPHA_TREK - ALPHA_TAVELO (hinten dünn, vorn dick).
  Außenwand = Regelfläche zwischen Trek-Kontur (Unterseite) und Tavelo-Kontur (Oberseite), je in ihrer Ebene.
  Alles, was entlang des Schafts läuft oder geschoben wird (Bohrung, Sichel, Gelenk-Zapfen),
  ist entlang der Schaftachse extrudiert.
  Achtung: axial_cylinder/axial_prism sind "geschert": Das Profil gilt in Ebenen parallel zur
  Unterseite, senkrecht zur Achse ist es längs um cos(ALPHA_TREK) gestaucht. Für Sichel und Gelenk
  ist das egal (Zapfen und Aufnahme gleich). Die Bohrung ist deshalb ein echter Zylinder um die Achse.

Aufruf (aus dem Repo-Wurzelverzeichnis):  python 02_CAD/adapter.py
  -> 02_CAD/out/Adapter_H20_T<aT>_V<aV>.*      Adapter zusammengebaut (Ansicht/Kontrolle)
  -> 02_CAD/out/DRUCK_Adapter_...stl/.3mf/.step  Drucklayout, beide Hälften getrennt
Danach: python 02_CAD/check_adapter.py (Wandstärken, Kollision), python 02_CAD/render_adapter.py
"""
import math
import numpy as np
import os
import cadquery as cq

# ---------------------------------------------------------------- Parameter
# Winkel
ALPHA_TREK = 17.0         # Neigung Trek-Auflageebene gegen Schaftnormale (geschätzt, am Prototyp 1 bestätigt: untere Fuge schließt)
ALPHA_TAVELO = 8.0        # gemessen 2026-09-28: Tavelo-Klemmbohrung 8° nach hinten gekippt bei flach aufliegender Sitzfläche

# Höhe
HEIGHT = 20.0             # Adapterhöhe entlang der Schaftachse (Durchstoßpunkt unten -> oben), wie ein Spacerstapel

# Schaft
STEERER_D = 28.6
STEERER_FLAT = 26.75      # seitliche Abflachungen (nur Info, Bohrung rund)
BORE_D = 30.0             # großzügig: Lage kommt von Trek-Nasen und Tavelo-Stiften, nicht vom Schaft (Prototyp 28,9 zu eng)
BORE_SLOT = 2.0           # Langloch: Hinterkante 2 weiter hinten, Vorderkante fest (Luft für den Vorbau)

# Außenkontur (Skizze V2; Freiform nach Vorgabe frei gestaltet)
REAR_X = 30.0
TIP_X = -28.0             # 13,0 ab vorderer Bohrungskante (bemaßt) + ~15
HALF_W = 19.75
BOTTOM_TIP_EXTRA = 2.5     # Unterseite: Spitze 2,5 weiter vorn als oben (Stirnwand vorn stärker geneigt)

# Trek-Nasen
NOSE_L, NOSE_W, NOSE_H = 7.6, 2.4, 1.5
NOSE_ANGLE = 24.0
NOSE_CX, NOSE_CY = 20.0, 7.9
POCKET_CLEAR = 0.3
POCKET_DEPTH = 2.5         # Taschentiefe (vorher 1,8)
POCKET_BRIDGE = 4.0        # Taschen vorn-innen zur Bohrung geöffnet (Steg wäre nur 0,27): Länge des Durchbruchs

# Kantenradien an Ober- und Unterseite
EDGE_R_BORE = 1.0          # Bohrung (Langloch)
EDGE_R_CHANNEL = 0.5       # Leitungskanal; größer macht die Wand zum vorderen Gelenk zu dünn (R1: 0,64)
EDGE_R_JUNCTION = 2.0      # innen: Übergang Langloch → Leitungskanal (Kante entlang der Achse)

# Leitungsschräge unten: Die hintere Bremsleitung kommt seitlich (rechts) aus dem Trek-Deckel. Auf beiden Seiten
# verläuft an der Unterseite ein Bogen von der äußersten Kanalecke zur breitesten Stelle des Langlochs; das Material
# innerhalb fällt schräg weg und läuft nach HOSE_SLOPE_H (entlang der Achse) aus. Oberseite unverändert.
HOSE_ARC_R = 45.0          # nach außen gewölbt; Außenwand unten dadurch min. ≈ 3,9 (Langloch sonst 4,74)
HOSE_SLOPE_H = 10.0
HOSE_EDGE_R = 0.5          # Kante Unterseite ↔ Schräge (R 1,0 lässt sich an den Enden nicht sauber verrunden)

# Leitungskanal
CRESCENT_FRONT_X = TIP_X + 6.8
CRESCENT_HALF_OUT = 22.75 / 2
CRESCENT_HALF_IN = 20.2 / 2

# Stifte oben (greifen in die Sacklöcher der Tavelo-Vorbauunterseite)
PIN_D, PIN_H = 3.0, 1.85
PIN_X = REAR_X - 42.0   # Prototyp: 40,5 → Adapter saß 1,5 zu weit vorn
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
    dict(x=-24.85, d=3.2, e=2.4, w=1.6),  # vorn, in der Wand vor der Sichel (Prototyp -24,1: nur 1,05 zum Kanal)
    dict(x=26.0, d=4.0, e=2.9, w=2.2),    # hinten, zwischen den Nasen
]

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
def bottom_outline_pts():
    """Trek-Kontur der Unterseite: wie die Tavelo-Kontur, aber die vordere Hälfte (x < 0) nach vorn gestreckt,
    sodass die Spitze um BOTTOM_TIP_EXTRA weiter vorn liegt. Quadratischer Verlauf: bei x = 0 tangential
    auslaufend, damit die hintere Hälfte unverändert bleibt."""
    return [(x - BOTTOM_TIP_EXTRA * (x / TIP_X) ** 2 if x < 0 else x, y) for (x, y) in outline_wire_pts()]


def envelope(aT, aV, h):
    """Regelfläche zwischen Trek-Kontur in der Unterseite (z=0, bottom_outline_pts) und Tavelo-Kontur in der Oberseite.
    Beide Konturen sind relativ zum jeweiligen Durchstoßpunkt der Schaftachse definiert."""
    P, n, u, d = top_frame(aT, aV, h)
    pts = outline_wire_pts()
    bottom = cq.Workplane("XY").spline(bottom_outline_pts(), periodic=True, includeCurrent=False).close().wire().val()
    top = (cq.Workplane("XY").spline(pts, periodic=True, includeCurrent=False).close()
           .rotate((0, 0, 0), (0, 1, 0), math.degrees(d)).translate(P).wire().val())
    return cq.Workplane("XY").add(cq.Solid.makeLoft([bottom, top], True))


def bore_cutter(aT):
    """Bohrung senkrecht zur Schaftachse rund (Ø BORE_D), als Langloch um BORE_SLOT nach hinten verlängert.
    Vorderkante fest bei BORE_D/2 vor der Achse. Richtung 'hinten' senkrecht zur Achse in der x-z-Ebene."""
    t = math.radians(aT)
    ax = cq.Vector(math.sin(t), 0, math.cos(t))
    back = cq.Vector(math.cos(t), 0, -math.sin(t))
    r, base, length = BORE_D / 2, ax * -30, 90
    s = cq.Solid.makeCylinder(r, length, base, ax)
    if BORE_SLOT > 0:
        s = s.fuse(cq.Solid.makeCylinder(r, length, base + back * BORE_SLOT, ax))
        box = (cq.Solid.makeBox(BORE_SLOT, BORE_D, length, pnt=cq.Vector(0, -r, 0))
               .rotate(cq.Vector(), cq.Vector(0, 1, 0), aT).translate(base))
        s = s.fuse(box)
    return cq.Workplane("XY").add(s.clean())


def crescent_pts():
    up = [(-10.5, CRESCENT_HALF_IN), (-13.5, CRESCENT_HALF_IN + 0.35), (-16.5, CRESCENT_HALF_IN + 0.8),
          (-18.9, CRESCENT_HALF_OUT), (-20.5, 9.6), (-21.1, 7.0), (CRESCENT_FRONT_X, 3.5)]
    return up + [(CRESCENT_FRONT_X, 0.0)] + [(x, -y) for (x, y) in reversed(up)]


def crescent_cutter(aT):
    return axial_prism(crescent_pts(), aT, -20, 60, spline=True, periodic=False)


def hose_cutters(aT=ALPHA_TREK, n=60):
    """Leitungsschräge unten (siehe HOSE_*), für y > 0 konstruiert und gespiegelt. Regelfläche zwischen dem Bogen
    in der Unterseite und der heutigen Innenkante (Kanal → Langloch) auf Höhe HOSE_SLOPE_H; nach innen ragt der
    Schnittkörper in den Hohlraum, damit keine deckungsgleichen Flächen entstehen."""
    if HOSE_ARC_R <= 0:
        return None
    t, c = math.tan(math.radians(aT)), math.cos(math.radians(aT))
    r = BORE_D / 2
    # Innenkante in der Unterseite (z = 0): Kanal ab seiner äußersten Ecke S nach hinten bis in die Bohrung,
    # dann Bohrungsrand (waagerechter Schnitt des Zylinders: Ellipse) bis zur breitesten Stelle E = (0, r)
    w = _wire(crescent_pts(), 0, 0, True, periodic=False)
    cp = [w.positionAt(u) for u in np.linspace(0, 1, 2000)]
    cp = [(v.x, v.y) for v in cp if v.y > 0.5]
    iS = max(range(len(cp)), key=lambda i: cp[i][1])
    side = cp[:iS + 1][::-1] if cp[0][0] > cp[iS][0] else cp[iS:]      # von S nach hinten
    path = []
    for x, y in side:
        if (x * c / r) ** 2 + (y / r) ** 2 < 1.0:                         # Kanal tritt in die Bohrung ein
            break
        path.append((x, y))
    th0 = math.atan2(path[-1][1], path[-1][0] * c)
    path += [(r * math.cos(a) / c, r * math.sin(a)) for a in np.linspace(th0, math.pi / 2, 200)][1:]
    P = np.array(path)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    C = np.c_[np.interp(np.linspace(0, seg[-1], n), seg, P[:, 0]), np.interp(np.linspace(0, seg[-1], n), seg, P[:, 1])]
    S, E = C[0], C[-1]
    # Bogen S → E, Radius HOSE_ARC_R, nach außen (+y) gewölbt
    m, d = (S + E) / 2, E - S
    L = np.hypot(*d)
    nrm = np.array([-d[1], d[0]]) / L
    if nrm[1] < 0:
        nrm = -nrm
    cen = m - nrm * math.sqrt(HOSE_ARC_R ** 2 - (L / 2) ** 2)
    a0, a1 = math.atan2(*(S - cen)[::-1]), math.atan2(*(E - cen)[::-1])
    da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    Arc = np.array([cen + HOSE_ARC_R * np.array([math.cos(a0 + da * k), math.sin(a0 + da * k)])
                    for k in np.linspace(0, 1, n)])
    inward = np.array([(-8.0, 0.0)]) - C
    inward /= np.linalg.norm(inward, axis=1)[:, None]
    zt = HOSE_SLOPE_H * c
    B = C + 0.2 * inward + [zt * t, 0]                                    # Ende der Schräge, knapp im Hohlraum

    def wire(z):
        f = z / zt
        q = Arc + (B - Arc) * f                                           # Regelfläche, linear in z
        back = (C + 2.0 * inward + [z * t, 0])[::-1]                      # Rückweg im Hohlraum
        V = lambda p: cq.Vector(p[0], p[1], z)
        edges = [cq.Edge.makeSpline([V(p) for p in q]), cq.Edge.makeLine(V(q[-1]), V(back[0])),
                 cq.Edge.makeSpline([V(p) for p in back]), cq.Edge.makeLine(V(back[-1]), V(q[0]))]
        return cq.Wire.assembleEdges(edges)

    right = cq.Solid.makeLoft([wire(-1.0), wire(zt)], True)
    return cq.Workplane("XY").add(right.fuse(right.mirror("XZ")).clean())


def nose_pocket_cutters(aT=ALPHA_TREK):
    """Taschen für die Trek-Nasen, senkrecht zur Unterseite. Das vordere (innere) Ende jeder Tasche liegt so nah an
    der Bohrung, dass nur ein 0,27-Steg bliebe; deshalb läuft von dort ein Durchbruch gleicher Breite zur Schaftachse."""
    L, W = NOSE_L + 2 * POCKET_CLEAR, NOSE_W + 2 * POCKET_CLEAR
    t = math.tan(math.radians(aT))
    ax_x = 0.5 * POCKET_DEPTH * t + BORE_SLOT / math.cos(math.radians(aT))   # Langloch-Hinterkreis, halbe Taschentiefe
    res = None
    for s in (1, -1):
        ang = 180.0 - NOSE_ANGLE if s == 1 else 180.0 + NOSE_ANGLE
        p = (cq.Workplane("XY").workplane(offset=-1.0)
             .center(NOSE_CX, s * NOSE_CY).slot2D(L, W, ang).extrude(POCKET_DEPTH + 1.0))
        if POCKET_BRIDGE > 0:
            a = math.radians(ang)
            cx = NOSE_CX + math.cos(a) * (L - W) / 2          # Mitte des vorderen Taschenendes
            cy = s * NOSE_CY + math.sin(a) * (L - W) / 2
            dx, dy = ax_x - cx, -cy
            n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
            br = (cq.Workplane("XY").workplane(offset=-1.0)
                  .center(cx + dx * POCKET_BRIDGE / 2, cy + dy * POCKET_BRIDGE / 2)
                  .slot2D(POCKET_BRIDGE + W, W, math.degrees(math.atan2(dy, dx))).extrude(POCKET_DEPTH + 1.0))
            p = p.union(br)
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
def core_body(aT=ALPHA_TREK, aV=ALPHA_TAVELO, h=HEIGHT):
    """Hülle minus Bohrung, Leitungskanal und Leitungsschräge. Verrundet: Kanten von Bohrung und Kanal an Ober- und
    Unterseite, die Kanten entlang der Achse am Übergang Langloch → Kanal und die Kante Unterseite ↔ Schräge."""
    from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
    bore, chan, hose = bore_cutter(aT), crescent_cutter(aT), hose_cutters(aT)
    cut = bore.union(chan)
    if hose is not None:
        cut = cut.union(hose)
    body = envelope(aT, aV, h).cut(cut).val()
    mk, n = BRepFilletAPI_MakeFillet(body.wrapped), 0

    def on(cutter, e):
        return cutter.distance(cq.Vertex.makeVertex(*e.positionAt(0.5).toTuple())) < 1e-4

    if EDGE_R_JUNCTION > 0:
        for e in body.Edges():
            if on(bore.val(), e) and on(chan.val(), e):
                mk.Add(EDGE_R_JUNCTION, e.wrapped); n += 1
    rules = [(bore.val(), EDGE_R_BORE), (chan.val(), EDGE_R_CHANNEL)]
    if hose is not None:
        rules.insert(0, (hose.val(), HOSE_EDGE_R))
    for f in body.Faces():
        if f.geomType() != "PLANE" or abs(f.normalAt().z) < 0.5:   # nur Ober- und Unterseite
            continue
        for e in f.Edges():
            for cutter, r in rules:
                if r > 0 and on(cutter, e):
                    mk.Add(r, e.wrapped); n += 1
                    break
    if n == 0:
        return cq.Workplane("XY").add(body)
    mk.Build()
    return cq.Workplane("XY").add(cq.Shape.cast(mk.Shape()))


def adapter(aT=ALPHA_TREK, aV=ALPHA_TAVELO, h=HEIGHT, with_joints=True):
    body = core_body(aT, aV, h).union(pins(aT, aV, h))
    A, B = split_halves(body, aT, h, with_joints)
    pockets = nose_pocket_cutters(aT)
    return A.cut(pockets), B.cut(pockets)


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
