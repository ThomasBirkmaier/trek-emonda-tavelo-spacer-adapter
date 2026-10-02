# CLAUDE.md

Zweiteiliger Spacer-Adapter zwischen dem Trek-Steuersatzdeckel (Émonda SL 6, 2024) und dem Tavelo-Avro-Rise-Cockpit. Parametrisches CadQuery-Modell. Was das Teil ist und wie man es druckt, steht in `README.md`. Maße, Entscheidungen, der Befund der Prototypen und die offenen Punkte stehen in `KONSTRUKTION.md`. **Lies zuerst `KONSTRUKTION.md`, Abschnitte 5 bis 7.**

## Arbeitsweise

- Doku und Kommentare auf Deutsch, technisch präzise; Annahmen als Annahmen kennzeichnen.
- Rev. D ist für die Bezugshöhe 22 am Rad bestätigt. Geometrie nur gezielt ändern und vorher die Folgen nennen, vor allem Wandstärken; Konflikte mit anderen Merkmalen sofort melden.
- Stand, Befunde und offene Punkte gehören in `KONSTRUKTION.md` (Abschnitte 6 bis 8), keine eigenen Status- oder Notizdateien.

## Befehle

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python 02_CAD/adapter.py          # Export nach 02_CAD/out/<Variante>/ (zusammengebaut + DRUCK_*-Layout)
python 02_CAD/check_adapter.py    # Kollision A∩B je Variante, Bohrungsmaß, Wandstärken (Warnung < 1,2 mm)
python 02_CAD/render_adapter.py   # 03_Renderings: Schnitte, Iso je Variante, Stiftschnitt, Drucklayout
```

Nach jeder Geometrieänderung alle drei in dieser Reihenfolge ausführen und Exporte und Renderings mitcommitten. Die Renderings immer ansehen. Die Dateinamen enthalten Bezugshöhe, Winkel (`TAG`, z. B. `_H22_T17_V7.2`) und Variante (`_Stift`, `_Passstift`); ändern sie sich, die alten Exporte per `git rm` entfernen. STEP und 3MF enthalten einen Zeitstempel: Bei einem reinen Doku- oder Kommentar-Commit die Exporte nicht mitcommitten (`git checkout -- 02_CAD/out/`).

## Geometrie: was man wissen muss

- Ursprung = Schaftachse ∩ Unterseite. **+x = hinten** (Klemmschraube des Vorbaus, Oberrohr), −x = vorn (Spitze, Leitungskanal). y quer, Teilung bei y = 0 (A: y > 0, B: y < 0). z = Normale der Unterseite.
- Schaftachse um α_T = 17° nach hinten geneigt. Oberseite (Tavelo) gemessen 8° gegen die Schaftnormale, nach Prototyp 2 korrigiert: um die Hinterkante gekippt, Spitze 0,8 höher (`TOP_FRONT_LIFT`) → α_V 7,21°, Keil 9,79°. `ALPHA_TAVELO` und `HEIGHT` werden daraus berechnet, nicht direkt setzen. `HEIGHT` (≈ `HEIGHT_REF` + 0,42) ist nur der Durchstoßpunkt der Achse; die Keilkorrektur hebt den Vorbau nicht (er lag hinten schon auf, der Spalt vorn wird gefüllt). Die Stapelhöhe stellt man über `HEIGHT_REF` ein (22).
- Die Außenwand ist eine Regelfläche zwischen der Kontur unten (`bottom_outline_pts`, vorn 2,5 länger) und oben (`outline_wire_pts`). Die **Oberseite muss exakt bleiben**, dort liegt der Vorbau passgenau auf.
- `axial_cylinder`/`axial_prism` sind geschert: Das Profil gilt parallel zur Unterseite und ist senkrecht zur Achse längs um cos 17° kürzer. Für Sichel und Gelenk ist das gewollt. Die **Bohrung** ist dagegen ein echter Zylinder (`bore_cutter`). Genau dieser Fehler hat Prototyp 1 am Schaft klemmen lassen.
- Die Lage bestimmen die Trek-Nasen (Taschen unten) und die Tavelo-Stifte (oben), nicht der Schaft.
- **Zwei Varianten** (`VARIANTS`), die beide gepflegt werden: `Passstift` (Sacklöcher `pin_holes` für eingeklebte Zylinderstifte Ø 3 × 8, auf dem Lochgrund: die Lochtiefe legt den Überstand fest) und `Stift` (angedruckt, `pins`). Alles andere ist identisch und kommt aus demselben `core_body`; Änderungen am Rest gelten immer für beide. Nur das Merkmal oben darf sich unterscheiden.
- Unterseitenkontur (`bottom_outline_pts`) ist an Prototyp 2 bündig bestätigt: nicht ändern; jede Änderung der Stützpunkte verschiebt den Spline auch hinten. Nasentaschen: 0,55 Spiel quer, 0,3 längs, 3 mm tief.
- Die Nasentaschen sind absichtlich zur Bohrung geöffnet (`POCKET_BRIDGE`). Innere Kanten oben und unten einheitlich `EDGE_R_INNER` = 0,5 (tangential verbundene Kanten lassen sich nur mit einem Radius verrunden). Der Übergang Langloch → Kanal (R 2,0) ist kein Fillet, sondern Teil des Schnitts (`junction_cutter`, `_inner_path`). Leitungsschräge unten (`hose_cutters`, `HOSE_*`): Bogen R 45 von der Kanalecke zur breitesten Stelle des Langlochs, untere Hälfte gerade, obere läuft tangential aus. Alles wird vor dem Verrunden abgezogen; Fillets an spitz auslaufenden oder fast tangentialen Kanten scheitern in OCC.
- **Richtungsregel Stifte:** Die Stifte stecken fest im Vorbau. Stifte im Adapter nach vorn → der Adapter wandert nach hinten, und umgekehrt.
- Gelenke können nur in den zwei Stegen auf y = 0 liegen (vorn vor dem Kanal, hinten hinter der Bohrung). Das hintere Gelenk liegt bereits im Gleichgewicht zwischen Hinterkante und Nasentasche.

## Ablage

- `01_Input/` enthält Rohdaten (Skizze, Fotos, Herstellerzeichnung). Nicht verändern.
- `02_CAD/adapter.py` ist die einzige Quelle der Geometrie. `02_CAD/out/` wird erzeugt, aber versioniert, damit man ohne Python drucken kann; je Variante ein Unterordner (`Passstift/`, `Stift/`).
- `03_Renderings/Hero.png` ist ein generiertes Aufmacherbild (Rev. C.4, Bildgenerator mit einer Modellansicht als Geometrievorlage), ohne Maßbezug. Alle anderen Bilder erzeugt `render_adapter.py`.
- Lizenz WTFPL.
