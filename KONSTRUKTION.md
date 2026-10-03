# Konstruktion

Adapter zwischen dem originalen Trek-Steuersatzdeckel (Émonda SL 6, 2024) und dem Tavelo-Avro-Rise-Cockpit.

**Stand:** Rev. D.1, 2026-10-03: Geometrie abgeschlossen für die Bezugshöhe 22 (unverändert seit Rev. D); Festigkeit mit FEM abgeschätzt (Abschnitt 9). Drei Prototypen gedruckt und am Rad geprüft (Abschnitt 6); Prototyp 3 (Variante Passstift) passt ohne weitere Korrektur. Zwei Varianten, die sich nur an den Stiften oben unterscheiden: **Passstift** (Sacklöcher für eingeklebte Zylinderstifte) und **Stift** (angedruckt), siehe D-12.

---

## 1. Schnittstellen

| ID | Schnittstelle | Gegenstück | Festlegung |
|---|---|---|---|
| IF-1 | Unterseite ↔ Trek-Deckel | originaler Trek-Deckel, bleibt unverändert | Kontur 60,5 × 39,5 (Spitze 2,5 weiter vorn als oben), zwei Nasen, Neigung α_T |
| IF-2 | Oberseite ↔ Tavelo-Vorbau | Vorbauunterseite (identisch zur Spacer-Sitzfläche) | Kontur 58 × 39,5, zwei Stifte in die Sacklöcher des Vorbaus (angedruckt oder als eingeklebte Zylinderstifte, D-12), Neigung α_V |
| IF-3 | Bohrung ↔ Gabelschaft | Carbonschaft Ø 28,6, seitlich abgeflacht auf 26,75 | Bohrung Ø 30 senkrecht zur Schaftachse, als Langloch 2 nach hinten verlängert (32 × 30), entlang der Schaftachse |
| IF-4 | Leitungsführung | 2 Bremsleitungen (Di2 funkt) | Tavelo-Kanal → Sichel → Öffnung im Trek-Deckel → Rahmen; die hintere Leitung kommt seitlich rechts aus dem Deckel (Leitungsschräge, D-11) |

## 2. Koordinatensystem

- **Ursprung:** Durchstoßpunkt der Schaftachse durch die Unterseite
- **x:** Längsachse, **+x nach hinten** (Richtung Oberrohr); Spitze vorn bei x = −28 (Oberseite) bzw. −30,5 (Unterseite)
- **y:** quer; Teilungsebene y = 0, Hälfte A bei y > 0, Hälfte B bei y < 0
- **z:** Normale der Unterseite
- **Schaftachse:** um α_T gegen z nach hinten geneigt

## 3. Maße (bemaßt; Skizze V2 plus Nachmessungen)

| Merkmal | Wert | Im Koordinatensystem |
|---|---|---|
| Kontur oben (Tavelo, in der Oberseite) | 58 × 39,5 | x = −28 … +30; y = ±19,75 |
| Kontur unten (Trek, in der Unterseite) | 60,5 × 39,5: vordere Hälfte nach vorn gestreckt, Spitze 2,5 weiter vorn; hintere Hälfte wie oben | x = −30,5 … +30 |
| Bohrungsmitte → Hinterkante | 30 | |
| vordere Bohrungskante → Spitze | 13,0 (Messmaß am Tavelo-Spacer, legt die Spitze fest) | |
| Sichel (Leitungskanal, zur Bohrung offen) | Vorderkante 6,8 hinter der Spitze; Breite außen 22,75 / innen 20,2 | x = −21,2; y = ±11,375 / ±10,1 |
| Stifte oben (Tavelo) | Ø 3 × 1,85; Abstand 28,75; 42,0 ab Hinterkante (Prototyp 1: 40,5, Adapter saß 1,5 zu weit vorn) | x = −12,0; y = ±14,375 (in der Oberseite) |
| Variante Passstift | Zylinderstift ISO 2338 Ø 3 m6 × 8, Edelstahl A2/A4, Überstand 1,85 (wie angedruckt), 6,15 im Loch; Sackloch Ø 3,0 × 6,15 ab Oberseite, Stift sitzt auf dem Grund, Fase 0,3 × 45° | gleiche Lage und Richtung wie die Stifte (senkrecht zur Oberseite) |
| Trek-Nasen | Langloch 7,6 × 2,4 × 1,5; äußerste Punkte 20,25 auseinander, innerste 11,35; Längsausdehnung 7,0 | Mitte x = +20,0; y = ±7,9; 24° zur Längsachse, V-förmig (vorn außen) |
| Taschen für die Nasen | Nase + 0,55 Spiel pro Seite quer (Breite 3,5) und 0,3 in Längsrichtung, Tiefe 3,0; vorderes (inneres) Ende zur Bohrung geöffnet (Durchbruch in Taschenbreite) | |
| Höhe | Bezug 22 entlang der Schaftachse (bis Prototyp 2: 20); rechnerisch 22,42 an der Achse durch die Keilkorrektur (D-6) | auf ebener Fläche gemessen: Hinterkante oben 16,3, Spitze oben 26,2 |

Die Skizze V2 in `01_Input/` nennt eine Gesamtlänge von 52,2; das war ein Messfehler, richtig sind 58 (13 + ~15 + 30).

Nasenwinkel abgeleitet: aus der Querausdehnung 23,2°, aus der Längsausdehnung 27,8°, beides erfüllt bei 24,0°. Die Maße sind auf ±0,2 konsistent; das Taschenspiel deckt die Unsicherheit ab.

## 4. Winkel und Keil

| Größe | Wert | Quelle |
|---|---|---|
| α_T: Trek-Sitzfläche gegen die Schaftnormale | **17°** | geschätzt (Trek-Stapel im Fahrbetrieb etwa waagerecht, Lenkwinkel ~73°), **an Prototyp 1 bis 3 bestätigt**: untere Fuge schließt |
| α_V: Tavelo-Sitzfläche gegen die Schaftnormale | **7,21°** (gemessen 8°, korrigiert) | gemessen: Klemmbohrung 8° nach hinten gekippt bei flach aufliegender Sitzfläche. Am Prototyp 2 klaffte oben vorn 0,8 zum Vorbau (Fühlerlehre, hinten dicht); die Oberseite ist deshalb um ihre Hinterkante gekippt, bis die Spitze 0,8 höher liegt (`TOP_FRONT_LIFT`): −0,79° |
| Keil zwischen Unter- und Oberseite | **α_T − α_V ≈ 9,8°** | hinten dünn, vorn dick |

Gegenprobe α_V (Stand vor der Korrektur nach Prototyp 2): Der Vorbau steht 80° zur Schaftachse und fällt damit relativ zur eigenen Sitzfläche um 2° ab. Am Émonda steigt die Sitzfläche 9° über die Horizontale, der Vorbau 7°. Das ist konsistent. Die gemessene „30-mm-Bohrung“ der Tavelo-Spacer ist Spiel (28,6 / cos 8° = 28,9). Der Adapter übernimmt die 30.

Der Lenkwinkel spielt für die Passung keine Rolle. Maßgeblich sind nur die Neigungen der Sitzflächen relativ zur Schaftachse.

## 5. Konstruktionsentscheidungen

| ID | Entscheidung | Begründung |
|---|---|---|
| D-1 | Bohrung Ø 30 senkrecht zur Schaftachse (0,7 Spiel radial zum Schaft Ø 28,6), als Langloch 2 nach hinten verlängert (32 × 30); Vorderkante 15 vor der Achse | Die Lage kommt von den Trek-Nasen unten und den Tavelo-Stiften oben, nicht vom Schaft. Das Langloch gibt dem Vorbau nach hinten Luft. Prototyp 1 (Ø 28,9, Kreise parallel zur Unterseite gezeichnet) war senkrecht zur Achse längs nur 27,6 und damit enger als der Schaft. Die Tavelo-Spacer haben ebenfalls 30. Wand zu den Stiften 1,6 (an der Kante R 0,5 oben; ohne Kantenradius 2,1), zu den Sacklöchern der Variante Passstift 1,3 (D-12). Die Nasentaschen sind zur Bohrung geöffnet (D-9). |
| D-2 | Außenwand = Regelfläche zwischen Trek-Kontur (unten) und Tavelo-Kontur (oben) | Beide Fugen schließen bündig, obwohl die Ebenen ≈ 10° gegeneinander stehen. |
| D-3 | Bohrung, Sichel und Gelenk entlang der Schaftachse | Das Teil wird entlang des Schafts gefügt, die Leitungen laufen parallel zum Schaft. Sichel und Gelenk sind als Profil parallel zur Unterseite definiert und entlang der Achse geschert, senkrecht zur Achse also längs um cos α_T kürzer; für sie ist das unerheblich. Die Bohrung ist ein echter Zylinder um die Achse (siehe D-1). |
| D-4 | Zweiteilig, Teilung bei y = 0 | Montage um Schaft und Leitungen, ohne die Hydraulik zu öffnen. |
| D-5 | **Gelenk nach Tavelo-Vorbild:** je Teilstelle zwei Zapfen mit Hals in Schlüssellochaufnahmen, unten von A nach B, oben von B nach A. Vorn: Ø 3,2 / Hals 1,6 / Versatz 2,4, bei x = −24,85 (Prototyp 1: −24,1; verschoben für mehr Wand zum Kanal). Kleinste Wand der vorderen Aufnahme zu Bohrung/Kanal 1,2 (oben, seit den Kantenradien D-10), unten 1,4. Hinten: Ø 4,0 / Hals 2,2 / Versatz 2,9, bei x = +26,0. Spiel 0,2 radial, 0,15 axial, Fuge 0,25 | Die Zapfen sperren quer. Gefügt wird durch Aufschieben von B entlang des Schafts. CAD-Kollisionstest: keine Überschneidung; quer blockiert ab ~0,5 mm; entlang des Schafts frei fügbar. |
| D-6 | Höhe 22 entlang der Schaftachse als Bezug (bis Prototyp 2: 20); durch die Korrektur der Oberseite (Kippen um die Hinterkante) liegt der Durchstoßpunkt der Achse bei 22,42 | ersetzt einen 20-mm-Spacerstapel und hebt den Vorbau um 2 mm: Der Schaft war so knapp gekürzt, dass die Top-Cap kaum Spalt für die Vorspannung hatte (O-8). Die 2 mm verschieben den Vorbau genau um 2,0 entlang der Achse (nachgerechnet); Winkel, Kontur, Stifte und Taschen bleiben. **Der Vorbau sitzt durch die Korrektur nicht höher:** Er lag am Prototyp 2 schon an der Hinterkante auf, und sein Winkel ist durch die Klemmung am Schaft fest; die Korrektur füllt nur den Spalt (vorher an der Spitze 0,80, an der Achse 0,41, an der Hinterkante 0). Nachgerechnet am Modell: Lage des Vorbaus alt ↔ neu entlang der Achse +0,0002 mm, neue Oberseite liegt auf 0,0000 mm in der Vorbau-Ebene. |
| D-7 | Werkstoff PA12 (MJF) für das Endteil empfohlen | Das Teil liegt in der Kraftkette der Lagervorspannung und wird warm. PETG (auch PETG-HF) kann unter dieser Last kriechen: dann lässt die Vorspannung nach, das Steuersatzspiel anfangs häufig prüfen. Kein PLA. |
| D-8 | Drucklayout: beide Hälften in einer Datei, getrennt, Unterseite auf dem Druckbett | ein Auftrag, keine verschränkten Teile im Druck |
| D-9 | Nasentaschen am vorderen (inneren) Ende zur Bohrung geöffnet: Durchbruch in Taschenbreite (3,5) Richtung Schaftachse, Tiefe wie die Tasche | Durch das Langloch bliebe nur ein Steg von 0,27, der beim Druck oder bei der Montage wegbricht. Offen gibt es keine losen Splitter; die Übergänge zur Bohrung sind stumpfwinklig. Die Nasen werden seitlich und am hinteren Ende geführt. |
| D-10 | Kantenradien: alle inneren Kanten an Ober- und Unterseite (Bohrung, Kanal, Übergang, Leitungsschräge) einheitlich R 0,5; der Übergang Langloch → Kanal entlang der Achse ist mit R 2,0 gerundet (als Teil des Schnitts, nicht als Verrundung) | Sauberes Aussehen, keine scharfen Kanten an den Leitungen. Einheitlich, weil die inneren Kanten tangential ineinander übergehen und sich so nur mit einem Radius verrunden lassen; R 1,0 würde die Wand zur oberen vorderen Gelenkaufnahme auf 0,64 senken (mit R 0,5: 1,21). Die R-2,0-Rundung ist im Schnitt konstruiert, damit die Leitungsschräge genau dieselbe Rundung trifft. |
| D-11 | Leitungsschräge an der Unterseite, beidseitig: Bogen R 45 (nach außen gewölbt) von der äußersten Ecke des Leitungskanals (x ≈ −18,5) zur breitesten Stelle des Langlochs (x = 0); das Material innerhalb fällt weg, bis zur halben Höhe der Schräge gerade, darüber läuft sie tangential (ohne Knick) in Kanal- und Bohrungswand aus, nach 10 mm entlang der Achse; Kante zur Unterseite R 0,5 | Die hintere Bremsleitung kommt seitlich rechts aus dem Trek-Deckel und bekommt so unten bis 3,4 mm mehr Luft. Oberseite unverändert. Außenwand an der Schräge min. ≈ 3,2 (Langloch sonst 4,74); die dünnsten Wände in diesem Bereich liegen weiterhin oben am Kanal (2,0) und an der vorderen Kanalecke (3,1) und werden nicht berührt. |
| D-12 | **Zwei Varianten**, sonst identisch (`VARIANTS`, ein gemeinsamer `core_body`): **Stift** mit angedruckten Stiften Ø 3 × 1,85; **Passstift** mit Sacklöchern Ø 3,0 × 6,15 (Fase 0,3) für Zylinderstifte ISO 2338 Ø 3 m6 × 8, Edelstahl, gleiche Lage und Richtung. Der Stift wird eingeklebt und sitzt auf dem Lochgrund: Die Lochtiefe legt den Überstand 1,85 fest | Stahlstifte sind belastbarer als angedruckte (bei FDM liegt am Fuß eine Schichtgrenze) und ergeben denselben Zapfen. Eingeklebt statt eingepresst: Ein Presssitz von 0,1 dehnt den Lochrand um ≈ 3 %, bei PETG im Bereich der Fließgrenze; die Wand zur Bohrung ist nur 1,3 bis 1,6. 8 mm Länge: 6,15 im Loch ≈ 2 × d reichen, der Stift trägt nur Querkräfte an der Oberseite; länger macht die Wand zur Bohrung dünner (10 mm: ≈ 1,46 statt 1,61 am Lochgrund). Wand Sackloch ↔ Bohrung 1,33 (nur oben an der Fase, darunter 1,6), ↔ Außenwand 1,77. Auf dem Grund statt mit Einstelllehre (Rev. C.6): kein Hilfsteil nötig. Der Überstand hängt dann an der Stiftlänge und an der Lage des gedruckten Lochgrunds (Schichthöhe, ≈ ±0,1–0,2); an Prototyp 3 passend. Ragt der Stift zu weit heraus, kann er in den (ungemessenen) Sacklöchern des Vorbaus aufsitzen. |

## 6. Befund der Prototypen

### Prototyp 1 (Rev. B.1, selbst gedruckt, am Rad anprobiert, 2026-09-29)

| Befund | Ursache | Änderung (Rev. C) |
|---|---|---|
| Winkel oben und unten passen, beide Fugen schließen (Prototyp 1 war nie vollständig montiert) | – | α_T = 17° und α_V = 8° vorerst bestätigt; α_V an Prototyp 2 korrigiert |
| Gelenk passt | – | vorderes Gelenk trotzdem 0,75 nach vorn (x = −24,85): Wand zum Leitungskanal 1,05 → 1,8 (später durch die Kantenradien 1,2, D-10) |
| Bohrung sehr schwer aufzuziehen, musste aufgefeilt werden | Kreise parallel zur Unterseite gezeichnet, senkrecht zur Achse längs nur 27,6 (Schaft 28,6) | Bohrung als echter Zylinder um die Achse, Ø 30, Langloch 2 nach hinten (D-1) |
| Adapter sitzt 1,5 zu weit vorn: steht vorn über den Vorbau, hinten fehlt Material | Stifte 1,5 zu weit hinten (Skizzenmaß 40,5 ab Hinterkante) | Stifte 42,0 ab Hinterkante (x = −12,0). Merkregel: Die Stifte sind im Vorbau fixiert; Stifte im Adapter nach vorn → Adapter wandert nach hinten |
| Seitlich kein Versatz | – | – |
| Taschen für die Trek-Nasen zu flach | – | Taschentiefe 1,8 → 2,5 |
| Untere Kante vorn muss weiter nach vorn | – | Unterseite vorn 2,5 länger (60,5); Oberseite exakt unverändert, weil dort der Vorbau passgenau aufliegt. Dadurch wird nur die Stirnwand vorn schräger |

### Prototyp 2 (Rev. C, FDM, 2026-10-01, montiert, Fühlerlehre)

| Befund | Ursache | Änderung |
|---|---|---|
| Oben vorn 0,8 Spalt zwischen Adapter und Vorbau, hinten dicht | Keil 0,79° zu flach (α_V-Messung) | Rev. C.2: Oberseite um ihre Hinterkante gekippt, Spitze 0,8 höher: α_V 7,21°, Keil 9,79°; der Spalt wird gefüllt, der Vorbau sitzt nicht höher (D-6) |
| Schaft so knapp gekürzt, dass die Top-Cap kaum Spalt für die Vorspannung hat; der Trek-Deckel ließ sich verdrehen | Schaftende zu hoch für 20 mm Stapel | Rev. C.3: Höhe 22 statt 20 (D-6) |
| Unten vorn dicht, hinten ein kurzer Abschnitt mit ≈ 0,15 Luft, danach dicht | örtlich, kein Winkelfehler | – |
| Hintere Unterkante schließt bündig mit dem Trek-Deckel | – | Unterseitenkontur nicht mehr ändern |
| Adapter setzt sich schwer bündig auf den Trek-Deckel | Nasentaschen knapp | Rev. C.4: Taschen 0,5 breiter, 3,0 tief |

### Prototyp 3 (Rev. C.6, Variante Passstift, PETG-HF, 2026-10-02, montiert)

| Befund | Ursache | Änderung |
|---|---|---|
| Passt: keine weitere Korrektur nötig | – | Rev. D: Geometrie wie C.6, Stand für die Bezugshöhe 22 abgeschlossen |

## 7. Offene Punkte

| ID | Punkt | Stand |
|---|---|---|
| O-1 | Wand zwischen Bohrungs-Langloch und Nasentaschen nur 0,27 | erledigt: Taschen zur Bohrung geöffnet (D-9) |
| O-2 | Feinschliff | erledigt: vorderes Gelenk verschoben (D-5), Taschen offen (D-9), Kantenradien (D-10) |
| O-3 | Prototyp 3 am Rad prüfen | erledigt: Variante Passstift passt (Abschnitt 6, Rev. D) |
| O-4 | Stahlstifte statt gedruckter Stifte | erledigt: Variante Passstift (D-12), eingeklebt statt eingepresst, weil ein Presssitz die Wand zur Bohrung (1,3 bis 1,6) überdehnen würde |
| O-5 | Idee: Einführfasen 0,3 an den angedruckten Stiften, 0,3–0,5 an den Enden der Gelenkzapfen | nicht umgesetzt; erleichtert das Fügen |
| O-6 | Idee: Gelenkspiel für MJF auf 0,25–0,3 (`JOINT_CLEAR`) | nicht umgesetzt; Einschätzung, kein Messwert. 0,2 hat im FDM-Prototyp gepasst |
| O-7 | Idee: „A“, „B“ und Revision innen einprägen; Oberfläche des Endteils gefärbt und dampfgeglättet | nicht umgesetzt |
| O-8 | Höhe 20 oder 22: Steht das Schaftende zu hoch, fehlt der Top-Cap der Spalt (Vorspannung) | erledigt: 22 (D-6, Rev. C.3) |
| O-9 | Teil in PA12 (MJF) oder gefräst | offen; das Teil in den finalen Maßen liegt in PETG-HF vor (Prototyp 3), die Geometrie von Rev. D gilt unverändert |
| O-10 | Andere Bezugshöhen (`HEIGHT_REF`) | nicht geprüft; abgeschlossen ist nur 22. Eine andere Höhe verschiebt den Vorbau entlang der Achse, Winkel und Kontur bleiben |
| O-11 | Langzeitverhalten in PETG-HF: Kriechen unter der Vorspannung, besonders bei Wärme (Abschnitt 9) | offen; Steuersatzspiel anfangs häufig prüfen |

Kräfte (FEM-Rechnung dazu in Abschnitt 9): Eine Kraft entlang der Schaftachse drückt den 9,79°-Keil mit ≈ 17 % der Normalkraft nach vorn (zum dicken Ende). Reibung an Ober- und Unterseite hält das zusammen schon ab μ ≈ 0,09 je Fläche; sonst tragen Nasen oder Stifte, und nach 2,7 (0,7 Spiel plus 2 Langloch) der Schaft. Flächenpressung bei 1 kN ≈ 1,2 MPa auf ≈ 405 mm² je Hälfte (≈ 810 mm² gesamt). Das Gelenk trägt keine Fahrlasten, jede Hälfte sitzt über eigene Nase und eigenen Stift. Lenk- und Biegemomente laufen über die Vorbauklemmung in den Schaft.

Prüfen nach jeder Änderung: `python 02_CAD/check_adapter.py` (Kollision der Hälften je Variante, Bohrungsmaß, Wandstärken).

## 8. Revisionen

| Rev. | Datum | Inhalt |
|---|---|---|
| B.1 | 2026-09-28 | α_V = 8° gemessen → Keil 9°; Höhe entlang der Schaftachse; Regelflächen-Außenwand; Drucklayout. Stand von Prototyp 1 |
| C | 2026-09-29 | Änderungen nach Prototyp 1 (Abschnitt 6); Taschen zur Bohrung geöffnet (D-9); Kantenradien (D-10) |
| C.1 | 2026-10-01 | Leitungsschräge an der Unterseite (D-11); Übergänge geglättet, Kantenradien einheitlich R 0,5 (D-10) |
| C.2 | 2026-10-01 | Keil nach Prototyp 2: Spitze oben 0,8 höher, α_V 7,21° (Spalt gefüllt, Vorbau unverändert) |
| C.3 | 2026-10-01 | Höhe 22 statt 20 (Spalt für die Top-Cap); Dateinamen `_H22_T17_V7.2` |
| C.4 | 2026-10-01 | Nasentaschen 0,5 breiter (Spiel quer 0,55 pro Seite) und 3,0 tief, damit der Adapter leichter bündig auf dem Trek-Deckel sitzt |
| C.5 | 2026-10-01 | Zweite Variante **Passstift** (Sacklöcher für eingeklebte Zylinderstifte, Lehre für den Überstand), sonst identisch mit **Stift** (D-12); Dateinamen mit Variante `_H22_T17_V7.2_Stift` / `_Passstift` |
| C.6 | 2026-10-01 | Passstift sitzt auf dem Grund: Sackloch 6,15 statt 7,15 tief, Lehre entfällt (D-12); je Variante ein Ordner in `02_CAD/out/` |
| D | 2026-10-02 | Prototyp 3 (Variante Passstift) passt: Geometrie unverändert wie C.6, Stand für die Bezugshöhe 22 abgeschlossen; Dokumentation für die Veröffentlichung überarbeitet, Fotos in `01_Input/` als JPEG |
| D.1 | 2026-10-03 | Festigkeitsabschätzung mit FEM (Abschnitt 9, `02_CAD/fem_adapter.py`): im Normalfall ausreichend fest, Voraussetzung trockene Auflageflächen, Variante Passstift bestätigt; Geometrie unverändert wie D |

## 9. Festigkeitsabschätzung (FEM)

Lineare FEM-Rechnung mit gmsh (quadratische Tetraeder C3D10) und CalculiX, Skript `02_CAD/fem_adapter.py`, Bilder `03_Renderings/FEM_*.png`. Das ist eine Plausibilisierung unter angenommenen Lasten, kein Festigkeitsnachweis.

**Mechanik.** Der Adapter ist ein Keil (9,79°) zwischen Vorbau und Trek-Deckel. Eine Kraft F entlang der Schaftachse drückt ihn mit ≈ 17 % der Normalkraft nach vorn, zum dicken Ende. Reibung oben und unten hält das zusammen schon ab μ ≈ 0,09 je Fläche; dann tragen Nasen und Stifte nichts. Ohne Reibung trägt entweder die Nase (am Trek-Deckel) oder der Stift (im Vorbau) die Keilkraft, je nachdem, wo das Spiel zuerst aufgebraucht ist (Nase 0,3 längs; Stift im Vorbau ungemessen). Der Schaft liegt in Schubrichtung erst nach 2,7 an (0,7 Spiel plus 2 Langloch).

**Modell**
- Last: **F = 3 kN** entlang der Achse als bewusst hoher Hüllwert (Vorspannung der Top-Cap plus Zusatzlast im Fahrbetrieb, wenn der Rahmen gegenüber der Gabel nach oben drückt; für Spacer gibt es keine Norm). Die Vorspannung allein liegt eher bei 0,3–1 kN (Annahme). Linear: Spannungen skalieren mit F.
- LF1 an Hälfte A: Die Hälften sind durch die Fuge getrennt und tragen je F/2 über ihre Flächen. LF2 bis LF4 am ganzen Ring, weil die Gelenke die Hälften quer koppeln; hier vereinfacht als starre Verbindung.
- Werkstoff isotrop linear-elastisch. **PETG-HF** (Bambu PETG HF TDS V1.0, 100 % Füllgrad, getempert): E 1810 / 1540 MPa, Zugfestigkeit 34 MPa in der Schicht, 23 MPa quer zu den Schichten, HDT 62 °C bei 1,8 MPa, Tg 66 °C. **PA12 MJF** (HP 3D HR PA12): E 1750 / 1950 MPa, Zugfestigkeit 50 / 51 MPa, HDT 104–108 °C bei 1,82 MPa. Druckrichtung Unterseite auf dem Bett: Die Schichten liegen parallel zur Unterseite, σ_zz ist die Spannung quer zu den Schichten.
- Netz 1,5 mm (0,4 an Rundungen), Hälfte ≈ 89 000, Ring ≈ 195 000 Knoten; quadratische Elemente mit geraden Kanten. Gegen 2,0 mm und (für LF1) 1,0 mm ändern sich Verschiebungen und 99,9-%-Werte um < 10 %. Stabil sind auch die Spitzen am Sackloch in LF4 (82,7 → 81,3 MPa); die Spitzen in LF2 und LF3 sitzen am Rand der Lagerung und werden über Nennwerte bewertet.
- Gegenproben: Reaktionskräfte = Last (LF1 438,6 / 0 / 1434,5 N = 1500 N · (sin 17°, 0, cos 17°); LF2/LF3 514 / 0 / 2980 N = N · (sin 9,79°, 0, cos 9,79°); LF4 quer 0, wie bei statisch bestimmter Lagerung gewollt). Mittlere Pressung oben 3,7 MPa bei 3 kN (≈ 405 mm² je Hälfte). Stiftfuß nach Biegeformel und FEM in derselben Größenordnung.

**Lastfälle und Ergebnisse** (F = 3 kN; bei 1 kN alle Spannungen durch 3)

| Lastfall | Annahme | maßgebender Wert | Ort | Sicherheit PETG-HF (in der Schicht / quer) | Sicherheit PA12 |
|---|---|---|---|---|---|
| LF1 Normalfall | Reibung trägt: Unterseite fest, Last entlang der Achse (verlangt unten μ ≈ 0,31, also konservativ) | σ1 8,8 MPa, σ_zz 2,9 MPa, Verformung 0,06 mm | Ecke der hinteren Gelenkaufnahme, Taschenrand | 3,9 / 7,9 | 5,7 |
| LF2 ohne Reibung, Nasen | Keilkraft 261 N je Seite an der hinteren Taschenstirn (Kontakt auf Nasenhöhe 1,5) | Pressung an der Nasenstirn nominell 72 MPa (FEM am Kontaktrand σ1 69, σ3 −80 MPa) | Nasentasche | bei 3 kN überlastet; bei 1 kN Pressung 24 MPa | bei 1 kN ≈ 2 |
| LF3 ohne Reibung, Passstift eingespannt | Stift im Vorbau fest, Lochwand unterhalb der Fase gehalten | σ1 22 MPa | Lochgrund | 1,6 / 3,6 | 2,3 |
| LF4 ohne Reibung, Passstift kippt | Querkraft 261 N je Stift in halber Überstandshöhe, Lagerdruck an der Mündung am größten | σ1 81 MPa, σ_zz 17 MPa | Lochflanke zur Bohrung (Wand 1,3) | 0,42 / 1,4 (bei 1 kN: 1,3 / 4,1) | 0,62 (bei 1 kN: 1,8) |
| LF3 Variante Stift | angedruckter Stift im Vorbau gehalten | σ1 97 MPa; nominell Schub im Fuß 37 MPa, bei kippendem Stift Biegung 91 MPa | Stiftfuß, in der Schichtebene | 0,35 (bei 1 kN: 1,05) | 0,52 (bei 1 kN: 1,6) |

**Bewertung**
- **Normalfall:** Unter Druck über die Flächen ist der Adapter unkritisch. Selbst bei 3 kN liegt die größte Zugspannung bei 9 MPa: rund 4-fache Reserve in PETG-HF (quer zu den Schichten fast 8-fach), knapp 6-fach in PA12. Die Verformung (0,06 mm) ist vernachlässigbar.
- **Voraussetzung sind trockene, fettfreie Auflageflächen.** Nur dann hält die Reibung die Keilkraft. Ohne Reibung trägt die Nase sie mit hoher Pressung an der Taschenstirn: Bei 3 kN wird die Stirn örtlich eingedrückt, bei der Vorspannung allein (≤ 1 kN, 24 MPa) bleibt es elastisch, kann in PETG aber kriechen; der Adapter würde sich dann um das Taschenspiel nach vorn setzen.
- **Passstift:** Ist der Stift im Vorbau eingespannt, ist das Sackloch unkritisch. Kann er kippen, konzentriert sich der Lagerdruck an der Lochmündung zur Bohrung hin (Wand 1,3): Bei 1 kN bleibt in PETG-HF nur 1,3-fache Reserve, bei 3 kN wird der Lochrand örtlich überlastet (er weitet sich, der Stift bleibt vom Vorbau gehalten). Das ist nur relevant, wenn die Reibung fehlt.
- **Angedruckter Stift:** Ohne Reibung würde er schon bei etwa 1 kN im Fuß abscheren oder abbrechen, und zwar in der Schichtgrenze (Schub 12 MPa, Biegung 30 MPa bei 1 kN gegen 23 MPa quer zu den Schichten). Das bestätigt D-12: Variante Passstift empfohlen.
- **Kriechen (nicht gerechnet, Abschätzung):** Die Vorspannung wirkt dauerhaft, die mittlere Pressung liegt bei 1 kN bei ≈ 1,2 MPa. PETG-HF hat seine Wärmeformbeständigkeit bei 62 °C und den Glasübergang bei 66 °C; ein schwarzes Teil in der Sonne kann 50–60 °C erreichen (Annahme). Dann kriecht PETG merklich, und die **Vorspannung lässt nach** (Steuersatzspiel), ohne dass das Teil bricht. Bei 1 kN wird der Spacer axial nur ≈ 0,015 mm zusammengedrückt (F · h / (E · A)); ist er das weichste Glied im verspannten Stapel (Annahme; ≈ 65 kN/mm, der Carbonschaft liegt vermutlich in ähnlicher Größenordnung), kann schon Kriechen von wenigen Tausendstelmillimetern einen spürbaren Teil der Vorspannung kosten. PA12 (HDT > 100 °C) ist hier deutlich unkritischer.

**Grenzen der Aussage:** linear-elastisch, isotrop, ohne Kontakt, ohne Reibung im Modell und ohne Kriechen; Kurzzeitfestigkeit der Datenblätter (ideale Probekörper; reale Drucke, besonders zwischen den Schichten, oft schwächer); der Vorbau drückt als gleichmäßige Flächenlast, nicht als steifer Körper; keine Ermüdung, kein Schlag; Lasten angenommen, nicht gemessen.

**Folgerung:** Im Normalfall ausreichend fest, auch in PETG-HF. Entscheidend sind trockene Auflageflächen und die Variante Passstift. In PETG-HF ist das Langzeitrisiko das Nachlassen der Vorspannung durch Kriechen; deshalb das Steuersatzspiel anfangs häufig prüfen, für den Dauerbetrieb PA12.
