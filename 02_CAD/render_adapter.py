"""Renderings des zweiteiligen Adapters: Schnitte in mehreren Höhen (Hälfte A blau, B orange), Iso/Explosion je Variante,
Detailschnitt durch die Stifte (beide Varianten), Drucklayout.
Aufruf:  python 02_CAD/render_adapter.py  (vorher python 02_CAD/adapter.py; das Drucklayout wird aus 02_CAD/out/Stift/DRUCK_*.stl gelesen)."""
import sys, os, math, tempfile, numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Repo-Wurzel, unabhängig vom Aufrufort
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "02_CAD"))
import adapter as ad, cadquery as cq

core = ad.core_body()
tmp = tempfile.mkdtemp()
meshes = {}
for var in ad.VARIANTS:
    for k, part in zip("AB", ad.adapter(variant=var, core=core)):
        f = os.path.join(tmp, f"{var}_{k}.stl")
        cq.exporters.export(part, f, tolerance=0.02, angularTolerance=0.1)
        meshes[var, k] = trimesh.load(f)
mA, mB = meshes["Stift", "A"], meshes["Stift", "B"]   # Schnitte: unterhalb der Stifte sind die Varianten gleich
H = ad.HEIGHT
cols = {"A": "tab:blue", "B": "tab:orange"}
zs = [(0.5, "z = 0,5: Unterseite, Taschen für Trek-Nasen"), (4.5, "z = 4,5: unterer Zapfen von A greift in B"),
      (13.0, "z = 13: oberer Zapfen von B greift in A")]
fig, axs = plt.subplots(1, 4, figsize=(22, 5.8))
# Seitenschnitt y = +8 (durch Hälfte A): zeigt Keil, Scherung, Nasentasche
ax = axs[3]
for m, k in ((mA, "A"),):
    s_ = m.section(plane_origin=[0, 8, 0], plane_normal=[0, 1, 0])
    for e in s_.discrete: ax.plot(e[:, 0], e[:, 2], "-", color=cols[k], lw=1.1)
aT = math.radians(ad.ALPHA_TREK)
ax.plot([-8 * math.sin(aT), 32 * math.sin(aT)], [-8 * math.cos(aT), 32 * math.cos(aT)], "r--", lw=0.8, label="Schaftachse")
ax.set_aspect("equal"); ax.grid(True, alpha=.35); ax.legend(fontsize=8, loc="upper left")
ax.set_title(f"Seitenschnitt y = 8: Keil {ad.ALPHA_TREK - ad.ALPHA_TAVELO:.2f}°, vorn = links", fontsize=10)
ax.set_xlabel("x in mm (+ hinten)"); ax.set_ylabel("z in mm"); ax.set_xlim(-34, 38); ax.set_ylim(-6, 30)
for ax, (z, t) in zip(axs[:3], zs):
    for m, k in ((mA, "A"), (mB, "B")):
        s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if s is not None:
            for e in s.discrete: ax.plot(e[:, 0], e[:, 1], "-", color=cols[k], lw=1.1)
    ax.axhline(0, color="k", lw=0.3, ls="--")
    ax.set_aspect("equal"); ax.grid(True, alpha=.35); ax.set_title(t, fontsize=10)
    ax.set_xlabel("x in mm (+ hinten)"); ax.set_xlim(-33, 36); ax.set_ylim(-22, 22)
fig.suptitle(f"Adapter {ad.TAG} – α_Trek {ad.ALPHA_TREK:g}°, α_Tavelo {ad.ALPHA_TAVELO:.2f}° – Hälfte A (y>0) blau, B (y<0) orange", fontsize=12)
fig.tight_layout(); fig.savefig("03_Renderings/Adapter_Schnitte.png", dpi=95)

def draw(ax, m, col, off, v):
    c = np.clip(0.3 + 0.7 * np.abs(m.face_normals @ v), 0, 1)[:, None]
    ax.add_collection3d(Poly3DCollection(m.triangles + off, facecolors=c * np.array(col) + (1 - c) * 0.08, edgecolor="none"))
for var in ad.VARIANTS:
    fig = plt.figure(figsize=(16, 7))
    for i, (el, az, t, ex) in enumerate([(28, -55, "Iso von vorn oben", 0), (22, -35, "Explosion: B wird von oben entlang des Schafts aufgeschoben", 1)]):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        e, a = np.radians(el), np.radians(az); v = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
        aT = math.radians(ad.ALPHA_TREK)
        offB = np.array([math.sin(aT), 0, math.cos(aT)]) * 16 * ex + np.array([0, -6, 0]) * ex
        draw(ax, meshes[var, "A"], (0.25, 0.5, 0.85), 0, v); draw(ax, meshes[var, "B"], (0.95, 0.55, 0.15), offB, v)
        ax.set_xlim(-32, 38); ax.set_ylim(-35, 35); ax.set_zlim(-10, 45); ax.set_box_aspect((70, 70, 55)); ax.view_init(el, az); ax.axis("off"); ax.set_title(t)
    fig.suptitle(f"Adapter {ad.TAG}, Variante {var}", fontsize=12)
    fig.tight_layout(); fig.savefig(f"03_Renderings/Adapter_Iso_{var}.png", dpi=95)

# Detailschnitt durch die Stiftachse (y = PIN_Y, Hälfte A), beide Varianten; Passstift eingezeichnet
P, n, u, d = ad.top_frame(ad.ALPHA_TREK, ad.ALPHA_TAVELO, ad.HEIGHT)
c0 = np.array([(P + u * ad.PIN_X).x, (P + u * ad.PIN_X).z]); nn = np.array([n.x, n.z]); uu = np.array([u.x, u.z])
fig, axs = plt.subplots(1, len(ad.VARIANTS), figsize=(12, 6))
for ax, var in zip(axs, ad.VARIANTS):
    s_ = meshes[var, "A"].section(plane_origin=[0, ad.PIN_Y, 0], plane_normal=[0, 1, 0])
    for e in s_.discrete: ax.plot(e[:, 0], e[:, 2], "-", color=cols["A"], lw=1.2)
    if var == "Passstift":   # Zylinderstift Ø 3 × DOWEL_L mit Überstand PIN_H
        lo_, hi_ = ad.PIN_H - ad.DOWEL_L, ad.PIN_H
        q = np.array([c0 + uu * x + nn * z for x, z in ((-1.5, lo_), (1.5, lo_), (1.5, hi_), (-1.5, hi_), (-1.5, lo_))])
        ax.plot(q[:, 0], q[:, 1], "-", color="0.35", lw=1.0, label=f"Zylinderstift Ø {ad.PIN_D:g} × {ad.DOWEL_L:g}")
        ax.legend(fontsize=8, loc="lower left")
        ax.set_title(f"Passstift: Sackloch Ø {ad.PINHOLE_D:g} × {ad.PINHOLE_DEPTH:.2f}, Fase {ad.PINHOLE_CHAMFER:g}, "
                     f"Überstand {ad.PIN_H:g}", fontsize=10)
    else:
        ax.set_title(f"Stift: angedruckt Ø {ad.PIN_D:g} × {ad.PIN_H:g}", fontsize=10)
    ax.set_aspect("equal"); ax.grid(True, alpha=.35)
    ax.set_xlim(c0[0] - 12, c0[0] + 14); ax.set_ylim(c0[1] - 12, c0[1] + 5)
    ax.set_xlabel("x in mm (+ hinten)"); ax.set_ylabel("z in mm")
fig.suptitle(f"Schnitt durch die Stiftachse y = {ad.PIN_Y:g} (Hälfte A), vorn = links; rechts davon die Bohrung", fontsize=12)
fig.tight_layout(); fig.savefig("03_Renderings/Stift_Varianten.png", dpi=95)

# Drucklayout: so, wie die Druckdatei auf dem Bauraum liegt (Unterseite auf z = 0)
mP = trimesh.load(f"02_CAD/out/Stift/DRUCK_Adapter_{ad.TAG}_Stift.stl")
lo, hi = mP.bounds
fig = plt.figure(figsize=(16, 7))
for i, (el, az, t) in enumerate([(45, -25, "Drucklayout, Iso"), (90, -90, "Drucklayout, Draufsicht")]):
    ax = fig.add_subplot(1, 2, i + 1, projection="3d")
    e, a = np.radians(el), np.radians(az); v = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    draw(ax, mP, (0.35, 0.35, 0.38), 0, v)
    c = (lo + hi) / 2; r = (hi - lo).max() / 2 + 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(0, 2 * r); ax.set_box_aspect((1, 1, 1))
    ax.view_init(el, az); ax.axis("off"); ax.set_title(t)
ext = hi - lo
fig.suptitle(f"Variante Stift (Passstift gleicher Bauraum): {ext[0]:.1f} × {ext[1]:.1f} × {ext[2]:.1f} mm, Unterseite (Trek-Auflage) auf dem Druckbett", fontsize=12)
fig.tight_layout(); fig.savefig("03_Renderings/Drucklayout_Adapter.png", dpi=95)
