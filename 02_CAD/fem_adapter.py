"""Festigkeitsabschätzung des Adapters mit linearer FEM (gmsh + CalculiX). Ergebnisse: KONSTRUKTION.md, Abschnitt 9.

Werkzeuge: gmsh (Vernetzung, quadratische Tetraeder) und CalculiX ccx (Solver, C3D10).
Aufruf:  python 02_CAD/fem_adapter.py [--variant Passstift|Stift] [--h 1.5 --hmin 0.4] [--force 3000] [--no-plots]
Ergebnis: Tabelle auf der Konsole, Bilder 03_Renderings/FEM_<Variante>_<LF>.png. Arbeitsdateien in einem temporären Ordner.

Mechanik: Der Adapter ist ein Keil (9,79°) zwischen Vorbau (oben) und Trek-Deckel (unten). Eine Kraft F entlang der
Schaftachse (Vorspannung der Top-Cap plus Zusatzlast im Fahrbetrieb) drückt ihn mit ≈ 17 % der Normalkraft nach vorn
(zum dicken Ende). Reibung oben und unten hält das zusammen schon ab μ ≈ 0,09 je Fläche; dann tragen Nasen und Stifte
nichts. Ohne Reibung muss entweder die Nase (Trek-Deckel) oder der Stift (Vorbau) die Keilkraft tragen.

Lastfälle:
  LF1 Normalfall   Hälfte A (die Hälften tragen je F/2 über ihre Flächen, die Fuge ist offen). Last entlang der Achse
                   als Flächenlast oben, Unterseite fest. Verlangt unten μ ≈ 0,31 und ist damit eine konservative
                   Spannungsrechnung für den Fall, dass Reibung trägt.
  LF2 Nase         ganzer Ring (die Gelenke koppeln die Hälften quer; hier vereinfacht als starre Verbindung), oben und
                   unten reibungsfrei: oben Normaldruck (axialer Anteil F), unten nur senkrecht gestützt; die Keilkraft
                   tragen die hinteren Stirnen der beiden Nasentaschen (Kontakthöhe = Nasenhöhe), quer gehalten an
                   je einem Knoten der Stege auf y = 0.
  LF3 Stift        wie LF2, aber die Keilkraft tragen die beiden Stifte, im Vorbau starr eingespannt: Wand des
                   Sacklochs (unterhalb der Fase) bzw. Mantel des angedruckten Stifts festgehalten.
  LF4 Stift kippt  nur Passstift: wie LF3, aber der Stift kann im Vorbau kippen (Spiel dort ungemessen): Querkraft je Stift
                   in Höhe PIN_H/2 über der Oberseite, Lagerdruck über die Tiefe linear (Kraft- und Momentengleichgewicht
                   des starren Stifts), über den Umfang ~ cos θ. Quer statisch bestimmt gelagert (Reaktionen ≈ 0).
Werkstoff isotrop linear-elastisch; Kontakt zum Schaft nicht angesetzt (in Schubrichtung 2,7 Spiel).
"""
import argparse
import math
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Repo-Wurzel, unabhängig vom Aufrufort
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "02_CAD"))
import adapter as A  # noqa: E402
import cadquery as cq  # noqa: E402
import gmsh  # noqa: E402

# Werkstoffe (Datenblätter; FDM: Probekörper 100 % Füllgrad, getempert). Schichten parallel zur Unterseite (z).
MATERIALS = {
    "PETG-HF": dict(E=1810.0, nu=0.38, Rm_xy=34.0, Rm_z=23.0),    # Bambu PETG HF TDS V1.0
    "PA12 MJF": dict(E=1750.0, nu=0.39, Rm_xy=50.0, Rm_z=50.0),   # HP 3D HR PA12
}
LOADCASES = ("LF1", "LF2", "LF3", "LF4")
WEDGE = math.radians(A.ALPHA_TREK - A.ALPHA_TAVELO)


# ---------------------------------------------------------------- Geometrie und Netz
def build(variant, ring):
    """ring=False: Hälfte A wie gedruckt. ring=True: ganzer Ring ohne Teilung (Hälften starr verbunden)."""
    if not ring:
        a, _ = A.adapter(variant=variant)
        return a.val()
    aT, aV, h = A.ALPHA_TREK, A.ALPHA_TAVELO, A.HEIGHT
    body = A.core_body(aT, aV, h)
    body = body.union(A.pins(aT, aV, h)) if variant == "Stift" else body.cut(A.pin_holes(aT, aV, h))
    return body.cut(A.nose_pocket_cutters(aT)).solids().val()


def mesh(shape, work, h, hmin):
    """Vernetzen (C3D10) und Randflächen über ihre Netzknoten zuordnen. Rückgabe: Knoten, Elemente, Dreiecksgruppen."""
    aT, aV, hh = A.ALPHA_TREK, A.ALPHA_TAVELO, A.HEIGHT
    P, n, _, _ = A.top_frame(aT, aV, hh)
    n, P = np.array(n.toTuple()), np.array(P.toTuple())
    pockets = A.nose_pocket_cutters(aT).val()
    holes = A.pin_holes(aT, aV, hh).val()
    pinsolid = A.pins(aT, aV, hh).val()
    step = os.path.join(work, "body.step")
    cq.exporters.export(cq.Workplane("XY").add(shape), step)
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.occ.importShapes(step)
    gmsh.model.occ.synchronize()
    for k, v in {"Mesh.MeshSizeMax": h, "Mesh.MeshSizeMin": hmin, "Mesh.MeshSizeFromCurvature": 16,
                 "Mesh.ElementOrder": 2, "Mesh.SecondOrderLinear": 1, "Mesh.Algorithm3D": 10}.items():
        # SecondOrderLinear: Mittelknoten auf der Kantenmitte (gerade Kanten); robuster als gekrümmte Elemente,
        # deren Optimierung am Stiftfuß abbrechen kann. Rundungen werden über die feine Elementgröße abgebildet.
        gmsh.option.setNumber(k, v)
    gmsh.model.mesh.generate(3)

    TOL = 0.05                                               # Mittelknoten gerader Kanten liegen neben gekrümmten Flächen

    def near(solid, pts):
        return all(solid.distance(cq.Vertex.makeVertex(*q)) < TOL for q in pts)

    groups = {g: [] for g in ("bottom", "top", "pocket", "pinhole", "pin")}
    for _, tag in gmsh.model.getEntities(2):
        pts = gmsh.model.mesh.getNodes(2, tag, includeBoundary=True)[1].reshape(-1, 3)
        smp = pts[np.linspace(0, len(pts) - 1, min(12, len(pts))).astype(int)]
        flat_z = np.ptp(pts[:, 2]) < 1e-4                    # waagerecht (z. B. Taschenboden)
        flat_n = np.ptp(pts @ n) < 1e-4                      # parallel zur Oberseite (Lochgrund, Stiftkopf)
        if np.all(np.abs(pts[:, 2]) < 1e-4):
            groups["bottom"].append(tag)
        elif np.all(np.abs((pts - P) @ n) < 1e-4):
            groups["top"].append(tag)
        elif not flat_z and near(pockets, smp):
            groups["pocket"].append(tag)
        elif not flat_n and near(holes, smp):
            groups["pinhole"].append(tag)
        elif not flat_n and near(pinsolid, smp) and np.all((smp - P) @ n > -1e-4):
            groups["pin"].append(tag)

    tags, xyz, _ = gmsh.model.mesh.getNodes()
    nodes = dict(zip(tags.astype(int), xyz.reshape(-1, 3)))
    et, _, enodes = gmsh.model.mesh.getElements(3)
    tets = enodes[list(et).index(11)].reshape(-1, 10).astype(int)
    tets = tets[:, [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]]           # gmsh → CalculiX: Kanten 3-4 und 2-4 tauschen
    faces = {}
    for g, tagl in groups.items():
        tri = []
        for t in tagl:
            et2, _, en2 = gmsh.model.mesh.getElements(2, t)
            tri.append(en2[list(et2).index(9)].reshape(-1, 6).astype(int))
        faces[g] = np.vstack(tri) if tri else np.zeros((0, 6), int)
    gmsh.finalize()
    return nodes, tets, faces, n, P


def tri_area(nodes, tri):
    p = np.array([nodes[k] for k in tri[:3]])
    return 0.5 * np.linalg.norm(np.cross(p[1] - p[0], p[2] - p[0]))


def traction_loads(nodes, tris, vec_per_area):
    """Konsistente Knotenlasten einer gleichmäßigen Flächenlast auf 6-Knoten-Dreiecken: Ecken 0, Kantenmitten A/3."""
    f = {}
    for tri in tris:
        a = tri_area(nodes, tri)
        for k in tri[3:]:
            f[k] = f.get(k, np.zeros(3)) + vec_per_area * a / 3.0
    return f


def bearing_loads(nodes, tris, n_top, P_top, force, s_from, s_to, e_arm):
    """Lagerdruck eines starren Stifts auf eine Zylinderfläche (Achse n_top) als Knotenlasten. Über den Umfang ~ cos θ auf
    der belasteten Seite; über die Tiefe s (ab Oberseite nach unten) linear, sodass Kraft und Moment einer Querkraft in
    Höhe e_arm über der Oberseite stimmen. Wo der lineare Verlauf negativ wird, drückt der Stift auf die Gegenseite."""
    F = np.linalg.norm(force)
    tdir = force / F
    L = s_to - s_from
    Mat = np.array([[L, L ** 2 / 2], [L ** 2 / 2, L ** 3 / 3]])
    qa, qb = np.linalg.solve(Mat, [F, -F * (e_arm + s_from)])   # q(s) = qa + qb (s - s_from)
    pts = np.array([nodes[k] for t in tris for k in t[:3]])
    ctr = pts.mean(axis=0)
    ctr = ctr - ((ctr - P_top) @ n_top) * n_top
    f, tot = {}, 0.0
    for tri in tris:
        c = np.mean([nodes[k] for k in tri[:3]], axis=0)
        sd = -float((c - P_top) @ n_top)
        if sd < s_from or sd > s_to:
            continue
        r = (c - ctr) - ((c - ctr) @ n_top) * n_top
        rn = np.linalg.norm(r)
        cos_t = float(r @ tdir) / rn
        q = qa + qb * (sd - s_from)
        w = max(cos_t, 0.0) if q > 0 else max(-cos_t, 0.0)
        vec = q * w / (2 * rn) * tdir                        # ∫ cos⁺ r dθ = 2 r
        a = tri_area(nodes, tri)
        for k in tri[3:]:
            f[k] = f.get(k, np.zeros(3)) + vec * a / 3.0
        tot += float(vec @ tdir) * a
    return {k: v * F / tot for k, v in f.items()}            # Diskretisierung: Kraftsumme exakt


def pocket_contact_nodes(nodes, faces):
    """Knoten der hinteren Taschenstirnen bis zur Nasenhöhe: dort liegt die Nase an, wenn der Keil nach vorn drückt."""
    L, W = A.NOSE_L + 2 * A.POCKET_CLEAR, A.NOSE_W + 2 * A.POCKET_CLEAR_W
    ends = []
    for s in (1, -1):
        a = math.radians(180.0 - A.NOSE_ANGLE if s == 1 else 180.0 + A.NOSE_ANGLE)
        d = np.array([math.cos(a), math.sin(a)])
        c = np.array([A.NOSE_CX, s * A.NOSE_CY])
        e1, e2 = c + d * (L - W) / 2, c - d * (L - W) / 2
        ends.append((e1, d) if e1[0] > e2[0] else (e2, -d))  # hinteres Ende und Richtung nach hinten
    out = set()
    for k in {k for t in faces["pocket"] for k in t}:
        p = nodes[k]
        if p[2] > A.NOSE_H + 1e-6:
            continue
        for e, d in ends:
            q = p[:2] - e
            if np.linalg.norm(q) < W / 2 + 0.05 and q @ d >= -1e-6:
                out.add(k)
    return sorted(out)


# ---------------------------------------------------------------- CalculiX
def write_inp(path, nodes, tets, faces, n_top, P_top, lc, F_total, mat):
    aT = math.radians(A.ALPHA_TREK)
    axis = np.array([math.sin(aT), 0.0, math.cos(aT)])
    top_area = sum(tri_area(nodes, t) for t in faces["top"])
    bottom = sorted({k for t in faces["bottom"] for k in t})
    fix = {}                                                 # Knoten → gesperrte Freiheitsgrade

    def lock(ks, dofs):
        for k in ks:
            fix.setdefault(k, set()).update(dofs)

    if lc == "LF1":                                          # Hälfte: Last entlang der Achse, Unterseite fest
        loads = traction_loads(nodes, faces["top"], -axis * (F_total / 2) / top_area)
        lock(bottom, (1, 2, 3))
    else:                                                    # Ring: oben nur Normaldruck, unten nur senkrecht
        N = F_total / float(n_top @ axis)
        loads = traction_loads(nodes, faces["top"], -n_top * N / top_area)
        lock(bottom, (3,))
        if lc == "LF2":
            lock(pocket_contact_nodes(nodes, faces), (1,))
            for x0 in (A.REAR_X, A.TIP_X - A.BOTTOM_TIP_EXTRA):   # quer halten: je ein Knoten der Stege auf y = 0
                k = min(bottom, key=lambda k: np.hypot(nodes[k][0] - x0, nodes[k][1]))
                lock([k], (2,))
        elif lc == "LF4":                                    # Stift kippt: Lagerdruck je Loch, quer statisch bestimmt
            d = WEDGE
            u = np.array([math.cos(d), 0.0, -math.sin(d)])   # in der Oberseite nach hinten
            T = N * math.tan(d) / 2                          # je Stift
            for side in (1, -1):
                tris = np.array([t for t in faces["pinhole"] if side * nodes[t[0]][1] > 0])
                for k, v in bearing_loads(nodes, tris, n_top, P_top, u * T, A.PINHOLE_CHAMFER,
                                          A.PINHOLE_DEPTH, A.PIN_H / 2).items():
                    loads[k] = loads.get(k, np.zeros(3)) + v
            kr = min(bottom, key=lambda k: np.hypot(nodes[k][0] - A.REAR_X, nodes[k][1]))
            kf = min(bottom, key=lambda k: np.hypot(nodes[k][0] - (A.TIP_X - A.BOTTOM_TIP_EXTRA), nodes[k][1]))
            lock([kr], (1, 2))
            lock([kf], (2,))
        else:
            if len(faces["pinhole"]):                        # Passstift: Lochwand unterhalb der Fase
                ks = [k for t in faces["pinhole"] for k in t
                      if -(nodes[k] - P_top) @ n_top > A.PINHOLE_CHAMFER + 1e-6]
            else:                                            # angedruckter Stift: Mantel im Vorbau
                ks = [k for t in faces["pin"] for k in t]
            lock(sorted(set(ks)), (1, 2))
    with open(path, "w") as fh:
        fh.write("*NODE\n")
        for k, p in nodes.items():
            fh.write(f"{k},{p[0]:.6f},{p[1]:.6f},{p[2]:.6f}\n")
        fh.write("*ELEMENT,TYPE=C3D10,ELSET=EALL\n")
        for i, t in enumerate(tets, 1):
            fh.write(f"{i}," + ",".join(map(str, t)) + "\n")
        fh.write(f"*MATERIAL,NAME=M\n*ELASTIC\n{mat['E']},{mat['nu']}\n*SOLID SECTION,ELSET=EALL,MATERIAL=M\n*BOUNDARY\n")
        for k, dofs in fix.items():
            for d in sorted(dofs):
                fh.write(f"{k},{d},{d}\n")
        fh.write("*STEP\n*STATIC\n*CLOAD\n")
        for k, v in loads.items():
            for d in range(3):
                if abs(v[d]) > 1e-12:
                    fh.write(f"{k},{d + 1},{v[d]:.8e}\n")
        fh.write("*NODE FILE\nU,RF\n*EL FILE\nS\n*END STEP\n")
    return set(fix)


def read_frd(path):
    """Knotenwerte aus der .frd: DISP, STRESS (SXX SYY SZZ SXY SYZ SZX), FORC (Reaktionskräfte)."""
    out, block = {}, None
    num = re.compile(r"-?\d\.\d+E[+-]\d\d")
    with open(path) as fh:
        for line in fh:
            if line.startswith(" -4"):
                block = line.split()[1]
                out[block] = {}
            elif line.startswith(" -1") and block:
                out[block][int(line[3:13])] = [float(x) for x in num.findall(line[13:])]
            elif line.startswith(" -3"):
                block = None
    return out


def evaluate(nodes, res, fixed):
    ks = np.array(sorted(res["STRESS"]))
    s = np.array([res["STRESS"][k][:6] for k in ks])
    T = np.zeros((len(s), 3, 3))
    T[:, 0, 0], T[:, 1, 1], T[:, 2, 2] = s[:, 0], s[:, 1], s[:, 2]
    T[:, 0, 1] = T[:, 1, 0] = s[:, 3]
    T[:, 1, 2] = T[:, 2, 1] = s[:, 4]
    T[:, 0, 2] = T[:, 2, 0] = s[:, 5]
    ev = np.linalg.eigvalsh(T)
    vm = np.sqrt(0.5 * ((ev[:, 0] - ev[:, 1]) ** 2 + (ev[:, 1] - ev[:, 2]) ** 2 + (ev[:, 2] - ev[:, 0]) ** 2))
    u = np.array([res["DISP"][k][:3] for k in ks])
    rf = np.array([v[:3] for k, v in res["FORC"].items() if k in fixed]).sum(axis=0)
    return dict(ks=ks, xyz=np.array([nodes[k] for k in ks]), vm=vm, s1=ev[:, 2], s3=ev[:, 0], szz=s[:, 2], u=u, rf=rf)


def hotspots(ev, key, n=3, sep=2.0):
    """Die n höchsten Werte an mindestens sep auseinanderliegenden Orten, mit nächstem Merkmal."""
    aT, aV, hh = A.ALPHA_TREK, A.ALPHA_TAVELO, A.HEIGHT
    feats = {"Sackloch/Stift": A.pin_holes(aT, aV, hh).union(A.pins(aT, aV, hh)).val(),
             "Nasentasche": A.nose_pocket_cutters(aT).val(),
             "Bohrung/Kanal": A.bore_cutter(aT).union(A.crescent_cutter(aT)).val()}
    out = []
    for i in np.argsort(-ev[key]):
        p = ev["xyz"][i]
        if all(np.linalg.norm(p - q) > sep for q, _, _ in out):
            vx = cq.Vertex.makeVertex(*p)
            d = {k: f.distance(vx) for k, f in feats.items()}
            near = min(d, key=d.get)
            out.append((p, ev[key][i], near if d[near] < 1.0 else ("Gelenk/Fuge" if abs(p[1]) < 5.5 else "Fläche")))
            if len(out) == n:
                break
    return out


def run(variant, h, hmin, F_total, work):
    results, geo = {}, {}
    for ring in (False, True):
        nodes, tets, faces, n_top, P_top = mesh(build(variant, ring), work, h, hmin)
        print(f"{'Ring' if ring else 'Hälfte A'}: {len(nodes)} Knoten, {len(tets)} C3D10; Flächen " +
              ", ".join(f"{g} {len(t)}" for g, t in faces.items()))
        geo[ring] = (nodes, tets)
        ring_lcs = ("LF2", "LF3", "LF4") if variant == "Passstift" else ("LF2", "LF3")
        for lc in (ring_lcs if ring else ("LF1",)):
            job = os.path.join(work, lc)
            fixed = write_inp(job + ".inp", nodes, tets, faces, n_top, P_top, lc, F_total, MATERIALS["PETG-HF"])
            r = subprocess.run(["ccx", "-i", job], cwd=work, capture_output=True, text=True)
            if r.returncode != 0 or not os.path.exists(job + ".frd"):
                print(r.stdout[-2000:], r.stderr[-2000:])
                raise SystemExit(f"ccx-Fehler in {lc}")
            ev = evaluate(nodes, read_frd(job + ".frd"), fixed)
            ev["ring"] = ring
            results[lc] = ev
    return results, geo


def report(results, F_total):
    N = F_total / math.cos(math.radians(A.ALPHA_TAVELO))
    print(f"\nLast: F = {F_total:.0f} N entlang der Schaftachse (LF1: Hälfte A mit F/2; LF2–LF4: Ring). "
          f"Keilkraft ohne Reibung {N * math.tan(WEDGE):.0f} N gesamt")
    print(f"{'LF':4s} {'σ1 max':>7s} {'σ_zz max':>8s} {'σ3 min':>7s} {'σ_vM 99,9%':>10s} {'|u| max':>8s}  Reaktion (Summe) N")
    for lc, ev in results.items():
        print(f"{lc:4s} {ev['s1'].max():7.1f} {ev['szz'].max():8.1f} {ev['s3'].min():7.1f} "
              f"{np.percentile(ev['vm'], 99.9):10.1f} {np.linalg.norm(ev['u'], axis=1).max():7.3f}mm  {np.round(ev['rf'], 1)}")
        for p, val, tag in hotspots(ev, "s1"):
            print(f"     σ1 {val:6.1f}  {tag:15s} (x {p[0]:.1f}, y {p[1]:.1f}, z {p[2]:.1f})")
    T = N * math.tan(WEDGE) / 2
    print(f"\nNennwerte ohne Reibung je Seite: Keilkraft {T:.0f} N; Pressung an der Nasenstirn (Nasenbreite × -höhe "
          f"{A.NOSE_W:g} × {A.NOSE_H:g}) {T / (A.NOSE_W * A.NOSE_H):.0f} MPa; Lochleibung Passstift (Ø × Tiefe) "
          f"{T / (A.PINHOLE_D * (A.PINHOLE_DEPTH - A.PINHOLE_CHAMFER)):.0f} MPa; Biegung am Fuß des angedruckten Stifts "
          f"{T * A.PIN_H / 2 / (math.pi * A.PIN_D ** 3 / 32):.0f} MPa, Schub im Fuß {T / (math.pi * A.PIN_D ** 2 / 4):.0f} MPa")
    print("\nSicherheit gegen Kurzzeitfestigkeit (Zug in der Schicht: Rm_xy/σ1; quer zu den Schichten: Rm_z/σ_zz):")
    for name, m in MATERIALS.items():
        print(f"  {name:9s} " + "; ".join(
            f"{lc} {m['Rm_xy'] / ev['s1'].max():.2f} / {m['Rm_z'] / max(ev['szz'].max(), 1e-9):.2f}"
            for lc, ev in results.items()))


def plot(geo, results, F_total, variant, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from collections import Counter
    for lc, ev in results.items():
        if variant != "Passstift" and lc != "LF3":           # LF1/LF2 gleichen der Variante Passstift
            continue
        nodes, tets = geo[ev["ring"]]
        cnt = Counter(tuple(sorted(f)) for t in tets for f in
                      ((t[0], t[1], t[2]), (t[0], t[1], t[3]), (t[0], t[2], t[3]), (t[1], t[2], t[3])))
        tris = [f for f, m in cnt.items() if m == 1]          # Außenflächen
        val = dict(zip(ev["ks"], ev["vm"]))
        vmax = float(np.percentile(ev["vm"], 99.9))
        cmap = plt.get_cmap("turbo")
        fig = plt.figure(figsize=(15, 6.5))
        ylo = -21 if ev["ring"] else -6
        for i, (el, az, t) in enumerate([(35, -70, "von vorn oben"), (-35, -110, "von vorn unten")]):
            ax = fig.add_subplot(1, 2, i + 1, projection="3d")
            Pp = np.array([[nodes[k] for k in tri] for tri in tris])
            c = np.array([np.mean([val.get(k, 0) for k in tri]) for tri in tris])
            ax.add_collection3d(Poly3DCollection(Pp, facecolors=cmap(np.clip(c / vmax, 0, 1)), edgecolor="none"))
            ax.set_xlim(-31, 37); ax.set_ylim(ylo, 21); ax.set_zlim(-1, 27); ax.set_box_aspect((68, 21 - ylo, 28))
            ax.view_init(el, az); ax.axis("off"); ax.set_title(t)
        fig.subplots_adjust(left=0.0, right=0.88, wspace=0.0)
        fig.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, vmax)), cax=fig.add_axes([0.9, 0.2, 0.015, 0.6]),
                     label="Vergleichsspannung von Mises in MPa")
        what = {"LF1": "Normalfall, Hälfte A", "LF2": "ohne Reibung, Nasen tragen",
                "LF3": "ohne Reibung, Stifte eingespannt", "LF4": "ohne Reibung, Stifte kippen"}[lc]
        fig.suptitle(f"FEM Variante {variant}, {lc} ({what}), F = {F_total:.0f} N entlang der Achse "
                     f"(Skala bis 99,9-%-Wert {vmax:.1f} MPa, Maximum {ev['vm'].max():.1f} MPa)", fontsize=11)
        fig.savefig(os.path.join(outdir, f"FEM_{variant}_{lc}.png"), dpi=90)
        plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="Passstift", choices=A.VARIANTS)
    ap.add_argument("--h", type=float, default=1.5, help="größte Elementkante, mm")
    ap.add_argument("--hmin", type=float, default=0.4, help="kleinste Elementkante, mm")
    ap.add_argument("--force", type=float, default=3000.0, help="Kraft entlang der Schaftachse, ganzer Adapter, N")
    ap.add_argument("--no-plots", action="store_true")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as work:
        results, geo = run(args.variant, args.h, args.hmin, args.force, work)
    report(results, args.force)
    if not args.no_plots:
        plot(geo, results, args.force, args.variant, "03_Renderings")
        print("Bilder: 03_Renderings/FEM_*.png")
