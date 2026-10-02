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
python 02_CAD/check_exports.py    # vor einem Release: passen die eingecheckten Exporte zum Code? (ändert nichts)
```

Nach jeder Geometrieänderung alle drei in dieser Reihenfolge ausführen und Exporte und Renderings mitcommitten. Die Renderings immer ansehen. Die Dateinamen enthalten Bezugshöhe, Winkel (`TAG`, z. B. `_H22_T17_V7.2`) und Variante (`_Stift`, `_Passstift`); ändern sie sich, die alten Exporte per `git rm` entfernen. STEP und 3MF enthalten einen Zeitstempel: Bei einem reinen Doku- oder Kommentar-Commit die Exporte nicht mitcommitten (`git checkout -- 02_CAD/out/`).

## Release („mache einen Release“)

Ein Release ist immer eine Revision aus der Tabelle in `KONSTRUKTION.md`, Abschnitt 8. Den Release selbst legt `.github/workflows/release.yml` auf GitHub an, sobald ein Tag `rev-<Revision>` gepusht wird: je Ordner in `02_CAD/out/` ein ZIP aus den eingecheckten Dateien, Titel „Rev. <Revision>“, Text aus der Tabellenzeile der Revision. Lokal wird nur der Tag gesetzt und gepusht.

Die Anweisung „mache einen Release“ ist die Freigabe, den Tag zu setzen und zu pushen. Bei jeder Unklarheit unten stattdessen anhalten und fragen.

1. **Ausgangslage prüfen:** `git fetch origin --tags`, dann `git status -sb`. Erwartet: Branch `main`, keine ungesicherten Änderungen, nicht hinter `origin/main`. Ist `main` vor `origin/main`, die Commits nennen und fragen, ob sie mit in den Release sollen (dann zuerst `git push origin main`).
2. **Revision bestimmen:** letzte Zeile der Revisionstabelle in `KONSTRUKTION.md` (z. B. `| D | 2026-10-02 | … |` → Revision `D`, Tag `rev-D`). Vorhandene Tags: `git tag -l 'rev-*'`.
   - Gibt es den Tag schon, ist diese Revision bereits veröffentlicht. Hat sich seit dem Tag etwas geändert (`git log rev-<R>..HEAD --oneline`), fragen, ob eine neue Revision eingetragen werden soll, und den Buchstaben bzw. die Nummer vorschlagen (nach `D` kommt `D.1` für Kleinigkeiten oder `E`). Ohne neue Zeile in der Tabelle keinen Release anlegen.
3. **Stimmigkeit prüfen:**
   - `README.md` nennt im Abschnitt „Stand“ dieselbe Revision; `KONSTRUKTION.md` ebenso in der Zeile „Stand“ oben.
   - `python 02_CAD/check_exports.py` muss mit „Exporte aktuell.“ enden (Exit-Code 0). Es baut beide Varianten neu und vergleicht exakt mit den eingecheckten STEP-Dateien, ohne `02_CAD/out/` anzufassen. Meldet es ABWEICHT, FEHLT oder VERALTET: anhalten und melden, nicht selbst neu exportieren. Gibt es noch keine Python-Umgebung, zuerst `.venv` anlegen und `requirements.txt` installieren (siehe Befehle); geht das nicht, den Punkt überspringen und das in der Rückmeldung sagen.
   - `python 02_CAD/check_adapter.py` muss ohne Fehler laufen (keine Überschneidung der Hälften).
4. **Tag setzen und pushen:** `git tag -a rev-<R> -m "Rev. <R>"` auf dem aktuellen `main`, dann `git push origin rev-<R>`.
5. **Ergebnis prüfen:** Mit der GitHub-CLI: `gh run watch` bzw. `gh run list --workflow Release --limit 1`, danach `gh release view rev-<R>` (zwei ZIPs `Passstift_Rev-<R>.zip`, `Stift_Rev-<R>.zip`). Ohne `gh` die Links nennen: `https://github.com/ThomasBirkmaier/trek-emonda-tavelo-spacer-adapter/actions` und `…/releases`.
6. **Wenn der Workflow scheitert:** Es entsteht kein Release. Fehler aus dem Log melden. Tag nur nach Rückfrage löschen und neu setzen (`git push --delete origin rev-<R>`, `git tag -d rev-<R>`).

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
