# CLAUDE.md

Zweiteiliger Spacer-Adapter zwischen dem Trek-Steuersatzdeckel (Émonda SL 6, 2024) und dem Tavelo-Avro-Rise-Cockpit. Parametrisches CadQuery-Modell. Was das Teil ist und wie man es druckt, steht in `README.md`. Maße, Entscheidungen, der Befund des Prototyps und die offenen Punkte stehen in `KONSTRUKTION.md`. **Lies zuerst `KONSTRUKTION.md`, Abschnitte 6 und 7.**

## Arbeitsweise mit Thomas

- Deutsch, du. Direkt und technisch präzise; Annahmen als Annahmen kennzeichnen.
- **Schritt für Schritt:** Thomas gibt jede Änderung einzeln vor. Nichts an Geometrie oder Doku ändern, bevor er die Änderung genannt oder freigegeben hat. Bei Rückfragen („sag mir erst …“) nur antworten, nichts umsetzen.
- **Nie ohne ausdrückliche Freigabe committen oder pushen.** Ungesicherte Änderungen bleiben liegen, bis er „commit“ sagt, auch wenn ein Hook meckert (dann höchstens `git stash`).
- Vor dem Umsetzen Folgen nennen, vor allem Wandstärken; Konflikte mit anderen Merkmalen sofort melden.
- Commits: Autor `Thomas Birkmaier <thomas.birkmaier@icloud.com>`, Nachricht auf Deutsch.

## Befehle

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python 02_CAD/adapter.py          # Export nach 02_CAD/out (zusammengebaut + DRUCK_*-Layout)
python 02_CAD/check_adapter.py    # Kollision A∩B, Bohrungsmaß, Wandstärken (Warnung < 1,2 mm)
python 02_CAD/render_adapter.py   # 03_Renderings: Schnitte, Iso, Drucklayout
```

Nach jeder Geometrieänderung alle drei in dieser Reihenfolge ausführen und Exporte und Renderings mitcommitten. Die Renderings immer ansehen. Die Dateinamen enthalten die Winkel (`_T17_V8`). STEP und 3MF enthalten einen Zeitstempel: Bei einem reinen Doku- oder Kommentar-Commit die Exporte nicht mitcommitten (`git checkout -- 02_CAD/out/`).

## Geometrie: was man wissen muss

- Ursprung = Schaftachse ∩ Unterseite. **+x = hinten** (Klemmschraube des Vorbaus, Oberrohr), −x = vorn (Spitze, Leitungskanal). y quer, Teilung bei y = 0 (A: y > 0, B: y < 0). z = Normale der Unterseite.
- Schaftachse um α_T = 17° nach hinten geneigt. Oberseite (Tavelo) 8° gegen die Schaftnormale, der Keil beträgt also 9°. Beide Winkel sind am Prototyp bestätigt.
- Die Außenwand ist eine Regelfläche zwischen der Kontur unten (`bottom_outline_pts`, vorn 2,5 länger) und oben (`outline_wire_pts`). Die **Oberseite muss exakt bleiben**, dort liegt der Vorbau passgenau auf.
- `axial_cylinder`/`axial_prism` sind geschert: Das Profil gilt parallel zur Unterseite und ist senkrecht zur Achse längs um cos 17° kürzer. Für Sichel und Gelenk ist das gewollt. Die **Bohrung** ist dagegen ein echter Zylinder (`bore_cutter`). Genau dieser Fehler hat den Prototyp am Schaft klemmen lassen.
- Die Lage bestimmen die Trek-Nasen (Taschen unten) und die Tavelo-Stifte (oben), nicht der Schaft.
- Die Nasentaschen sind absichtlich zur Bohrung geöffnet (`POCKET_BRIDGE`). Innere Kanten oben und unten einheitlich `EDGE_R_INNER` = 0,5 (tangential verbundene Kanten lassen sich nur mit einem Radius verrunden). Der Übergang Langloch → Kanal (R 2,0) ist kein Fillet, sondern Teil des Schnitts (`junction_cutter`, `_inner_path`). Leitungsschräge unten (`hose_cutters`, `HOSE_*`): Bogen R 45 von der Kanalecke zur breitesten Stelle des Langlochs, untere Hälfte gerade, obere läuft tangential aus. Alles wird vor dem Verrunden abgezogen; Fillets an spitz auslaufenden oder fast tangentialen Kanten scheitern in OCC.
- **Richtungsregel Stifte:** Die Stifte stecken fest im Vorbau. Stifte im Adapter nach vorn → der Adapter wandert nach hinten, und umgekehrt.
- Gelenke können nur in den zwei Stegen auf y = 0 liegen (vorn vor dem Kanal, hinten hinter der Bohrung). Das hintere Gelenk liegt bereits im Gleichgewicht zwischen Hinterkante und Nasentasche.

## Ablage

- `01_Input/` enthält Rohdaten (Skizze, Fotos, Herstellerzeichnung). Nicht verändern.
- `02_CAD/adapter.py` ist die einzige Quelle der Geometrie. `02_CAD/out/` wird erzeugt, aber versioniert, damit man ohne Python drucken kann.
- `03_Renderings/Hero.png` ist ein generiertes Aufmacherbild (Rev. C, Bildgenerator mit einer Modellansicht als Geometrievorlage), ohne Maßbezug. Alle anderen Bilder erzeugt `render_adapter.py`.
- Keine Status-, Auftrags- oder Notizdateien anlegen. Stand und offene Punkte gehören in `KONSTRUKTION.md` (Abschnitte 6 bis 8).
- Lizenz WTFPL.

## Arbeitskopien

GitHub (`ThomasBirkmaier/trek-emonda-tavelo-spacer-adapter`, Branch `main`) ist die Referenz. Thomas' Arbeitskopie liegt auf seinem Mac unter `~/Documents/Projects/Coding/Emonda Tavelo Spacer Adapter`. Arbeitet eine Cloud-Session ohne Push-Recht vom Mac aus, geht der Abgleich per `git bundle`: Bundle in den Repo-Root legen (nicht nach `.git`), `git fetch <bundle> main`, dann fast-forward, danach das Bundle löschen. `*.bundle` ist ignoriert. Auf dem Mac `git --no-optional-locks status` verwenden, damit keine `index.lock` liegen bleibt. PNGs nie einzeln per Dateiübertragung auf den Mac schreiben (sie bekommen dabei einen C2PA-Metadatenblock und gelten für Git als geändert), sondern per Bundle oder als Archiv.
