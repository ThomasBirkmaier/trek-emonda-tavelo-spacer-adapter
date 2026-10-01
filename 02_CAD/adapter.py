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
  -> 02_CAD/out/<Variante>/Adapter_<TAG>_<Variante>.*                  zusammengebaut (Ansicht/Kontrolle), TAG = H<Höhe>_T<aT>_V<aV>
  -> 02_CAD/out/<Variante>/DRUCK_Adapter_<TAG>_<Variante>.stl/.3mf/.step  Drucklayout, beide Hälften getrennt
  Varianten (VARIANTS): Stift = angedruckte Stifte, Passstift = Sacklöcher für Zylinderstifte; sonst identisch.
Danach: python 02_CAD/check_adapter.py (Wandstärken, Kollision), python 02_CAD/render_adapter.py
"""
import math
import numpy as np
import os
import cadquery as cq

# ---------------------------------------------------------------- Parameter
# Winkel
ALPHA_TREK = 17.0         # Neigung Trek-Auflageebene gegen Schaftnormale (geschätzt, am Prototyp 1 bestätigt: untere Fuge schließt)
ALPHA_TAVELO_MEAS = 8.0   # gemessen 2026-09-28: Tavelo-Klemmbohrung 8° nach hinten gekippt bei flach aufliegender Sitzfläche
HEIGHT_REF = 22.0         # Adapterhöhe entlang der Schaftachse beim gemessenen Winkel (bis Prototyp 2: 20; +2 für den Spalt der Top-Cap)

# Korrektur aus Prototyp 2 (Fühlerlehre, montiert): oben vorn 0,8 Spalt zum Vorbau, hinten dicht. Die Oberseite wird
# um ihre Hinterkante gekippt, bis die Spitze TOP_FRONT_LIFT höher liegt; Winkel und Höhe ergeben sich daraus.
# Der Vorbau sitzt dadurch NICHT höher: Er lag schon an der Hinterkante auf, sein Winkel ist durch die Klemmung am Schaft
# fest; es wird nur der Spalt gefüllt. HEIGHT (≈ HEIGHT_REF + 0,42) ist nur der neue Durchstoßpunkt der Achse durch die Oberseite,
# dort war vorher ≈ 0,41 Luft. Nachgerechnet: Vorbau-Lage alt ↔ neu entlang der Achse +0,0002 mm.
TOP_FRONT_LIFT = 0.8

# Schaft
STEERER_D = 28.6
STEERER_FLAT = 26.75      # seitliche Abflachungen (nur Info, Bohrung rund)
BORE_D = 30.0             # großzügig: Lage kommt von Trek-Nasen und Tavelo-Stiften, nicht vom Schaft (Prototyp 28,9 zu eng)
BORE_SLOT = 2.0           # Langloch: Hinterkante 2 weiter hinten, Vorderkante fest (Luft für den Vorbau)

# Außenkontur (Skizze V2; Freiform nach Vorgabe frei gestaltet)
REAR_X = 30.0
TIP_X = -28.0             # 13,0 ab vorderer Bohrungskante (bemaßt) + ~15
HALF_W = 19.75


def _top_from_lift(aT, aV0, h0, lift):
    """Oberseite um ihre Hinterkante (REAR_X vor dem Achsdurchstoß, in der Oberseite) kippen, bis die Spitze (TIP_X)
    um lift höher liegt. Rückgabe: neuer Tavelo-Winkel und neue Höhe entlang der Achse."""
    da = math.degrees(math.atan2(lift, REAR_X - TIP_X))
    aV = aV0 - da
    tT = math.radians(aT)
    ax = (math.sin(tT), math.cos(tT))
    d0, d1 = math.radians(aT - aV0), math.radians(aT - aV)
    rear = (h0 * ax[0] + REAR_X * math.cos(d0), h0 * ax[1] - REAR_X * math.sin(d0))   # Hinterkante (x, z)
    n1 = (math.sin(d1), math.cos(d1))                                                   # neue Normale
    h = (rear[0] * n1[0] + rear[1] * n1[1]) / (ax[0] * n1[0] + ax[1] * n1[1])
    return aV, h


ALPHA_TAVELO, HEIGHT = _top_from_lift(ALPHA_TREK, ALPHA_TAVELO_MEAS, HEIGHT_REF, TOP_FRONT_LIFT)
TAG = f"H{HEIGHT_REF:g}_T{round(ALPHA_TREK, 1):g}_V{round(ALPHA_TAVELO, 1):g}"   # für Dateinamen (Bezugshöhe, s. u.)
BOTTOM_TIP_EXTRA = 2.5     # Unterseite: Spitze 2,5 weiter vorn als oben (Stirnwand vorn stärker geneigt)

# Trek-Nasen
NOSE_L, NOSE_W, NOSE_H = 7.6, 2.4, 1.5
NOSE_ANGLE = 24.0
NOSE_CX, NOSE_CY = 20.0, 7.9
POCKET_CLEAR = 0.3         # Spiel pro Seite in Längsrichtung der Tasche
POCKET_CLEAR_W = 0.55      # Spiel pro Seite quer (Prototyp 2: 0,3; +0,5 Breite, damit der Adapter leichter bündig aufsitzt)
POCKET_DEPTH = 3.0         # Taschentiefe (Prototyp 1: 1,8; Prototyp 2: 2,5)
POCKET_BRIDGE = 4.0        # Taschen vorn-innen zur Bohrung geöffnet (Steg wäre nur 0,27): Länge des Durchbruchs

# Kantenradien an Ober- und Unterseite
EDGE_R_INNER = 0.5         # alle inneren Kanten an Ober- und Unterseite (Bohrung, Kanal, Rundung, Schräge); einheitlich,
                           # weil OCC tangential verbundene Kanten nur mit einem Radius verrundet; größer macht die
                           # Wand zum vorderen Gelenk zu dünn (R 1: 0,64)
EDGE_R_JUNCTION = 2.0      # innen: Übergang Langloch → Leitungskanal (Kante entlang der Achse)

# Leitungsschräge unten: Die hintere Bremsleitung kommt seitlich (rechts) aus dem Trek-Deckel. Auf beiden Seiten
# verläuft an der Unterseite ein Bogen von der äußersten Kanalecke zur breitesten Stelle des Langlochs; das Material
# innerhalb fällt schräg weg und läuft nach HOSE_SLOPE_H (entlang der Achse) aus. Oberseite unverändert.
HOSE_ARC_R = 45.0          # nach außen gewölbt; Außenwand unten dadurch min. ≈ 3,9 (Langloch sonst 4,74)
HOSE_SLOPE_H = 10.0

# Leitungskanal
CRESCENT_FRONT_X = TIP_X + 6.8
CRESCENT_HALF_OUT = 22.75 / 2
CRESCENT_HALF_IN = 20.2 / 2

# Stifte oben (greifen in die Sacklöcher der Tavelo-Vorbauunterseite)
PIN_D, PIN_H = 3.0, 1.85
PIN_X = REAR_X - 42.0   # Prototyp: 40,5 → Adapter saß 1,5 zu weit vorn
PIN_Y = 28.75 / 2

# Varianten: Alles außer den Stiften ist identisch.
#   "Stift"      Stifte angedruckt (bisherige Ausführung)
#   "Passstift"  Sacklöcher für Zylinderstifte ISO 2338 Ø 3 m6 × DOWEL_L (Edelstahl), eingeklebt und bis auf den Grund
#                gedrückt; die Lochtiefe legt den Überstand PIN_H fest. Der Stift ergibt denselben Zapfen wie "Stift".
VARIANTS = ("Stift", "Passstift")
DOWEL_L = 8.0                            # Stiftlänge; 6,15 im Loch ≈ 2 × d, länger macht die Wand zur Bohrung dünner
PINHOLE_D = 3.0                          # gedruckt; vor dem Kleben mit 3,0 nachbohren (FDM druckt Löcher zu klein)
PINHOLE_DEPTH = DOWEL_L - PIN_H          # ab Oberseite; Stift sitzt auf dem Grund, Überstand = PIN_H
PINHOLE_CHAMFER = 0.3                    # Fase 45° oben

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


def _inner_path(aT=ALPHA_TREK):
    """Innenkante in der Unterseite (z = 0), rechte Hälfte: Kanal ab seiner äußersten Ecke S nach hinten bis in die
    Bohrung, dann Bohrungsrand (waagerechter Schnitt des Zylinders: Ellipse) bis zur breitesten Stelle E = (0, r).
    Die Ecke Kanal → Bohrung ist mit EDGE_R_JUNCTION abgerundet (tangential, Bézier).
    Rückgabe: Pfad (N×2) und die Rundung (Ecke, Bézierpunkte) bzw. None."""
    c = math.cos(math.radians(aT))
    r = BORE_D / 2
    w = _wire(crescent_pts(), 0, 0, True, periodic=False)
    us = np.linspace(0, 1, 4000)
    cp = [(w.positionAt(u), w.tangentAt(u)) for u in us]
    cp = [((v.x, v.y), (tg.x, tg.y)) for v, tg in cp if v.y > 0.5]
    iS = max(range(len(cp)), key=lambda i: cp[i][0][1])
    if cp[0][0][0] > cp[iS][0][0]:                                        # von S nach hinten
        side = [(p, (-tg[0], -tg[1])) for p, tg in cp[:iS + 1][::-1]]
    else:
        side = cp[iS:]
    path, tang = [], []
    for (x, y), tg in side:
        if (x * c / r) ** 2 + (y / r) ** 2 < 1.0:                         # Kanal tritt in die Bohrung ein
            break
        path.append((x, y)); tang.append(tg)
    k = len(path) - 1                                                     # Eckpunkt Kanal → Bohrung
    th0 = math.atan2(path[-1][1], path[-1][0] * c)
    for a in np.linspace(th0, math.pi / 2, 400)[1:]:                      # Ellipse, Richtung zur Oberseite
        path.append((r * math.cos(a) / c, r * math.sin(a))); tang.append((r * math.sin(a) / c, -r * math.cos(a)))
    P = np.array(path)
    Tg = np.array(tang); Tg /= np.linalg.norm(Tg, axis=1)[:, None]
    if EDGE_R_JUNCTION <= 0:
        return P, None
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    phi = math.acos(max(-1.0, min(1.0, float(Tg[k] @ Tg[k + 1]))))
    Lt = EDGE_R_JUNCTION * math.tan(phi / 2)
    i1 = int(np.searchsorted(d, d[k] - Lt)); i2 = int(np.searchsorted(d, d[k] + Lt))
    T1, T2, t1, t2 = P[i1], P[i2], Tg[i1], Tg[i2]                         # Berührpunkte und exakte Tangenten
    ang = math.acos(max(-1.0, min(1.0, float(t1 @ t2))))
    Rb = np.linalg.norm(T2 - T1) / (2 * math.sin(max(ang, 1e-3) / 2))   # Radius des Ersatzkreises
    a_ = 4 / 3 * math.tan(ang / 4) * Rb                                  # Hebellänge Kreisnäherung
    c1, c2 = T1 + t1 * a_, T2 - t2 * a_                                   # kubische Bézier, tangential an beide Kurven
    bez = np.array([(1 - q) ** 3 * T1 + 3 * (1 - q) ** 2 * q * c1 + 3 * (1 - q) * q ** 2 * c2 + q ** 3 * T2
                    for q in np.linspace(0, 1, 30)])
    return np.vstack([P[:i1], bez, P[i2 + 1:]]), (P[k].copy(), bez)


def junction_cutter(aT=ALPHA_TREK):
    """Rundung der Kante Langloch → Kanal (entlang der Achse), als Schnittkörper statt als Verrundung, damit die
    Leitungsschräge exakt dieselbe Rundung trifft. Beidseitig."""
    _, rnd = _inner_path(aT)
    if rnd is None:
        return None
    corner, bez = rnd
    tip = corner + (corner - bez.mean(axis=0)) * 0.5                      # Ecke etwas in den Hohlraum verlängert
    t = math.tan(math.radians(aT))

    def wire(z):
        V = lambda p: cq.Vector(p[0] + z * t, p[1], z)
        return cq.Wire.assembleEdges([cq.Edge.makeSpline([V(p) for p in bez]), cq.Edge.makeLine(V(bez[-1]), V(tip)),
                                      cq.Edge.makeLine(V(tip), V(bez[0]))])

    right = cq.Solid.makeLoft([wire(-20.0), wire(60.0)], True)
    return cq.Workplane("XY").add(right.fuse(right.mirror("XZ")).clean())


def hose_cutters(aT=ALPHA_TREK, n=60):
    """Leitungsschräge unten (siehe HOSE_*), für y > 0 konstruiert und gespiegelt. Fläche zwischen dem Bogen in der
    Unterseite und der Innenkante (Kanal → Langloch, mit Rundung) auf Höhe HOSE_SLOPE_H: untere Hälfte gerade,
    obere Hälfte läuft tangential in die Wand aus; nach innen ragt der Schnittkörper in den Hohlraum, damit keine deckungsgleichen Flächen entstehen."""
    if HOSE_ARC_R <= 0:
        return None
    t, c = math.tan(math.radians(aT)), math.cos(math.radians(aT))
    P, _ = _inner_path(aT)
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
    W = C + 0.3 * inward                                                 # Innenkante, knapp im Hohlraum
    off = Arc - W                                                         # waagerechter Versatz an der Unterseite

    f0 = 0.5                                                              # bis hier gerade, danach tangentialer Auslauf

    def wire(z):
        # Versatz: bis f0 linear (saubere Kante unten), danach quadratisch auf null, tangential an die Wand (kein Knick)
        f = z / zt
        hh = 1 - 2 / (1 + f0) * f if f <= f0 else (1 - f) ** 2 / (1 - f0 ** 2)
        q = W + [z * t, 0] + off * hh
        back = (C + 2.0 * inward + [z * t, 0])[::-1]                      # Rückweg im Hohlraum
        V = lambda p: cq.Vector(p[0], p[1], z)
        edges = [cq.Edge.makeSpline([V(p) for p in q]), cq.Edge.makeLine(V(q[-1]), V(back[0])),
                 cq.Edge.makeSpline([V(p) for p in back]), cq.Edge.makeLine(V(back[-1]), V(q[0]))]
        return cq.Wire.assembleEdges(edges)

    zs = [-1.0, 0.0, f0 * zt] + list(np.linspace(f0, 1.0, 7)[1:] * zt)
    right = cq.Solid.makeLoft([wire(z) for z in zs], False)
    return cq.Workplane("XY").add(right.fuse(right.mirror("XZ")).clean())


def nose_pocket_cutters(aT=ALPHA_TREK):
    """Taschen für die Trek-Nasen, senkrecht zur Unterseite. Das vordere (innere) Ende jeder Tasche liegt so nah an
    der Bohrung, dass nur ein 0,27-Steg bliebe; deshalb läuft von dort ein Durchbruch gleicher Breite zur Schaftachse."""
    L, W = NOSE_L + 2 * POCKET_CLEAR, NOSE_W + 2 * POCKET_CLEAR_W
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


def pin_holes(aT, aV, h):
    """Sacklöcher für die Passstifte: gleiche Lage und Richtung wie pins(), Tiefe PINHOLE_DEPTH ab Oberseite,
    Fase PINHOLE_CHAMFER × 45° oben. Schnittkörper ragt 1 über die Oberseite hinaus."""
    P, n, u, d = top_frame(aT, aV, h)
    r, k = PINHOLE_D / 2, PINHOLE_CHAMFER
    res = None
    for s in (1, -1):
        c = P + u * PIN_X + cq.Vector(0, s * PIN_Y, 0)
        hole = cq.Solid.makeCylinder(r, PINHOLE_DEPTH + 1.0, cq.Vector(0, 0, -PINHOLE_DEPTH), cq.Vector(0, 0, 1))
        if k > 0:
            hole = hole.fuse(cq.Solid.makeCone(r, r + k + 1.0, k + 1.0, cq.Vector(0, 0, -k), cq.Vector(0, 0, 1)))
        hole = cq.Workplane("XY").add(hole.clean()).rotate((0, 0, 0), (0, 1, 0), math.degrees(d)).translate(c)
        res = hole if res is None else res.union(hole)
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
    """Hülle minus Bohrung, Leitungskanal, Rundung am Übergang Langloch → Kanal und Leitungsschräge.
    Danach die inneren Kanten an Ober- und Unterseite verrundet."""
    from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
    bore, chan = bore_cutter(aT), crescent_cutter(aT)
    extra = [x for x in (junction_cutter(aT), hose_cutters(aT)) if x is not None]
    cut = bore.union(chan)
    for x in extra:
        cut = cut.union(x)
    body = envelope(aT, aV, h).cut(cut).solids().val()
    cv = cut.val()
    mk, n = BRepFilletAPI_MakeFillet(body.wrapped), 0
    for f in body.Faces():
        if f.geomType() != "PLANE" or abs(f.normalAt().z) < 0.5:   # nur Ober- und Unterseite
            continue
        for e in f.Edges():
            if cv.distance(cq.Vertex.makeVertex(*e.positionAt(0.5).toTuple())) < 1e-4:
                mk.Add(EDGE_R_INNER, e.wrapped); n += 1
    if n == 0 or EDGE_R_INNER <= 0:
        return cq.Workplane("XY").add(body)
    mk.Build()
    return cq.Workplane("XY").add(cq.Shape.cast(mk.Shape()))


def adapter(aT=ALPHA_TREK, aV=ALPHA_TAVELO, h=HEIGHT, with_joints=True, variant="Stift", core=None):
    """variant: siehe VARIANTS. Beide Varianten entstehen aus demselben core_body; core kann übergeben werden."""
    body = core_body(aT, aV, h) if core is None else core
    if variant == "Stift":
        body = body.union(pins(aT, aV, h))
    elif variant == "Passstift":
        body = body.cut(pin_holes(aT, aV, h))
    else:
        raise ValueError(f"unbekannte Variante {variant!r}, erlaubt: {VARIANTS}")
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
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    core = core_body()
    for var in VARIANTS:
        out = os.path.join(root, var)                    # je Variante ein Ordner
        os.makedirs(out, exist_ok=True)
        A, B = adapter(variant=var, core=core)
        v = export_pair(A, B, os.path.join(out, f"Adapter_{TAG}_{var}"))
        print(f"Adapter {var}", "Körper A/B:", len(A.solids().vals()), len(B.solids().vals()), "Volumen %.0f mm3" % v)
        bb = export_print_layout(A, B, os.path.join(out, f"DRUCK_Adapter_{TAG}_{var}"))
        print("  Drucklayout Bauraum %.1f x %.1f x %.1f mm" % (bb.xlen, bb.ylen, bb.zlen))
