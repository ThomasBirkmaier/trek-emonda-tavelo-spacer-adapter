"""Renderings des zweiteiligen Adapters: Schnitte in mehreren Höhen (Hälfte A blau, B orange), Iso/Explosion, Drucklayout.
Vorher python 02_CAD/adapter.py ausführen (das Drucklayout wird aus 02_CAD/out/DRUCK_*.stl gelesen)."""
import sys, math, numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
sys.path.insert(0, "02_CAD")
import adapter as ad, cadquery as cq

A, B = ad.adapter()
cq.exporters.export(A, "/tmp/A.stl", tolerance=0.02, angularTolerance=0.1)
cq.exporters.export(B, "/tmp/B.stl", tolerance=0.02, angularTolerance=0.1)
mA, mB = trimesh.load("/tmp/A.stl"), trimesh.load("/tmp/B.stl")
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
ax.set_title(f"Seitenschnitt y = 8: Keil {ad.ALPHA_TREK - ad.ALPHA_TAVELO:g}°, vorn = links", fontsize=10)
ax.set_xlabel("x in mm (+ hinten)"); ax.set_ylabel("z in mm"); ax.set_xlim(-34, 38); ax.set_ylim(-6, 30)
for ax, (z, t) in zip(axs[:3], zs):
    for m, k in ((mA, "A"), (mB, "B")):
        s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if s is not None:
            for e in s.discrete: ax.plot(e[:, 0], e[:, 1], "-", color=cols[k], lw=1.1)
    ax.axhline(0, color="k", lw=0.3, ls="--")
    ax.set_aspect("equal"); ax.grid(True, alpha=.35); ax.set_title(t, fontsize=10)
    ax.set_xlabel("x in mm (+ hinten)"); ax.set_xlim(-33, 36); ax.set_ylim(-22, 22)
fig.suptitle(f"Adapter H{H:g} – α_Trek {ad.ALPHA_TREK:g}°, α_Tavelo {ad.ALPHA_TAVELO:g}° – Hälfte A (y>0) blau, B (y<0) orange", fontsize=12)
fig.tight_layout(); fig.savefig("03_Renderings/Adapter_H20_Schnitte.png", dpi=95)

fig = plt.figure(figsize=(16, 7))
def draw(ax, m, col, off, v):
    c = np.clip(0.3 + 0.7 * np.abs(m.face_normals @ v), 0, 1)[:, None]
    ax.add_collection3d(Poly3DCollection(m.triangles + off, facecolors=c * np.array(col) + (1 - c) * 0.08, edgecolor="none"))
for i, (el, az, t, ex) in enumerate([(28, -55, "Iso von vorn oben", 0), (22, -35, "Explosion: B wird von oben entlang des Schafts aufgeschoben", 1)]):
    ax = fig.add_subplot(1, 2, i + 1, projection="3d")
    e, a = np.radians(el), np.radians(az); v = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    aT = math.radians(ad.ALPHA_TREK)
    offB = np.array([math.sin(aT), 0, math.cos(aT)]) * 16 * ex + np.array([0, -6, 0]) * ex
    draw(ax, mA, (0.25, 0.5, 0.85), 0, v); draw(ax, mB, (0.95, 0.55, 0.15), offB, v)
    ax.set_xlim(-32, 38); ax.set_ylim(-35, 35); ax.set_zlim(-10, 45); ax.set_box_aspect((70, 70, 55)); ax.view_init(el, az); ax.axis("off"); ax.set_title(t)
fig.tight_layout(); fig.savefig("03_Renderings/Adapter_H20_Iso.png", dpi=95)

# Drucklayout: so, wie die Druckdatei auf dem Bauraum liegt (Unterseite auf z = 0)
mP = trimesh.load(f"02_CAD/out/DRUCK_Adapter_H{H:g}_T{ad.ALPHA_TREK:g}_V{ad.ALPHA_TAVELO:g}.stl")
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
fig.suptitle(f"Bauraum {ext[0]:.1f} × {ext[1]:.1f} × {ext[2]:.1f} mm, Unterseite (Trek-Auflage) auf dem Druckbett", fontsize=12)
fig.tight_layout(); fig.savefig("03_Renderings/Drucklayout_Adapter.png", dpi=95)
