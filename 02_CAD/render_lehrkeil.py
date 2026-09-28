"""Rendering eines Lehrkeils: Schnitte parallel zur Auflageebene (Hälfte A blau, B orange)."""
import sys, numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, "02_CAD")
import adapter as ad, cadquery as cq

alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 17.0
A, B = ad.gauge(alpha)
cq.exporters.export(A, "/tmp/gA.stl"); cq.exporters.export(B, "/tmp/gB.stl")
ms = {"A": trimesh.load("/tmp/gA.stl"), "B": trimesh.load("/tmp/gB.stl")}
cols = {"A": "tab:blue", "B": "tab:orange"}
fig, axs = plt.subplots(1, 3, figsize=(17, 5.6))
for ax, (z, t) in zip(axs, [(0.5, "Unterseite: Taschen für Trek-Nasen"), (2.5, "Mitte: Bohrung, Sichel, Teilung"), (4.6, "über Oberseite: Stifte Ø3")]):
    for k, m in ms.items():
        s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if s is not None:
            for e in s.discrete: ax.plot(e[:, 0], e[:, 1], "-", color=cols[k], lw=1.1)
    ax.axhline(0, color="k", lw=0.3, ls="--"); ax.set_aspect("equal"); ax.grid(True, alpha=.35)
    ax.set_title(t, fontsize=10); ax.set_xlabel("x in mm (+ hinten)"); ax.set_xlim(-31, 34); ax.set_ylim(-22, 22)
fig.suptitle(f"Lehrkeil {alpha:g}° – 4 mm, zweiteilig ohne Gelenk", fontsize=12)
fig.tight_layout(); fig.savefig(f"03_Renderings/Lehrkeil_{alpha:g}deg_Schnitte.png", dpi=95)
