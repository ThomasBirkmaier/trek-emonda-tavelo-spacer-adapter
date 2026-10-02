"""Prüft, ob die eingecheckten Exporte in 02_CAD/out/ zum aktuellen Code passen (vor einem Release).

Baut beide Varianten neu und vergleicht sie mit den eingecheckten STEP-Dateien über exakte B-Rep-Kenngrößen
(Volumen, Oberfläche, Schwerpunkt). Das ist unabhängig von der Triangulierung, also auch mit einer anderen
CadQuery-/OCC-Version verlässlich, und erkennt schon kleine Änderungen (z. B. eine Fase). Außerdem müssen zu jedem
Export STL, STEP (und beim Drucklayout 3MF) vorhanden sein, und es darf keine veralteten Dateien geben.
02_CAD/out/ bleibt unverändert.

Aufruf:  python 02_CAD/check_exports.py      (Exit-Code 1, wenn ein Export fehlt, abweicht oder veraltet ist)
"""
import atexit
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Repo-Wurzel, unabhängig vom Aufrufort
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "02_CAD"))
import adapter as A  # noqa: E402
import cadquery as cq  # noqa: E402

TOL_VOL = 0.05    # mm³    (eine Fase 0,3 → 0,25 an den Sacklöchern ändert die Oberfläche um ≈ 0,5 mm²)
TOL_AREA = 0.05   # mm²
TOL_COM = 2e-3    # mm


def props_via_step(solids, path):
    """Kenngrößen nach dem Weg über STEP, damit neu gebaute und eingecheckte Geometrie gleich behandelt werden."""
    cq.exporters.export(cq.Workplane("XY").add(solids), path)
    return props(cq.importers.importStep(path).solids().vals())


def props(solids):
    vol = sum(s.Volume() for s in solids)
    area = sum(s.Area() for s in solids)
    com = sum((cq.Shape.centerOfMass(s) * s.Volume() for s in solids), cq.Vector()) / vol
    return vol, area, com


ok = True
tmp = tempfile.mkdtemp()
atexit.register(shutil.rmtree, tmp, ignore_errors=True)
core = A.core_body()
known = set()
for var in A.VARIANTS:
    a, b = A.adapter(variant=var, core=core)
    gap = 8.0                                   # wie export_print_layout
    layouts = {f"Adapter_{A.TAG}_{var}": (a.solids().vals() + b.solids().vals(), ("stl", "step")),
               f"DRUCK_Adapter_{A.TAG}_{var}": (a.translate((0, gap, 0)).solids().vals()
                                                + b.translate((0, -gap, 0)).solids().vals(), ("stl", "step", "3mf"))}
    for stem, (solids, exts) in layouts.items():
        base = os.path.join("02_CAD", "out", var, stem)
        known |= {f"{var}/{stem}.{e}" for e in exts}
        missing = [e for e in exts if not os.path.exists(f"{base}.{e}")]
        if missing:
            print(f"FEHLT    {base}.{{{','.join(missing)}}}")
            ok = False
            continue
        v_new, a_new, c_new = props_via_step(solids, os.path.join(tmp, stem + ".step"))
        v_ref, a_ref, c_ref = props(cq.importers.importStep(f"{base}.step").solids().vals())
        dc = (c_new - c_ref).Length
        good = abs(v_new - v_ref) <= TOL_VOL and abs(a_new - a_ref) <= TOL_AREA and dc <= TOL_COM
        ok &= good
        print(f"{'ok      ' if good else 'ABWEICHT'} {base}   Volumen {v_ref:.3f} → {v_new:.3f} mm³, "
              f"Oberfläche {a_ref:.3f} → {a_new:.3f} mm², Schwerpunkt Δ {dc:.5f} mm")
for var in sorted(os.listdir(os.path.join("02_CAD", "out"))):
    for f in sorted(os.listdir(os.path.join("02_CAD", "out", var))):
        if f"{var}/{f}" not in known:
            print(f"VERALTET 02_CAD/out/{var}/{f} (gehört zu keinem aktuellen Export)")
            ok = False
print("Exporte aktuell." if ok else "Exporte passen NICHT zum Code: python 02_CAD/adapter.py ausführen und mitcommitten.")
sys.exit(0 if ok else 1)
