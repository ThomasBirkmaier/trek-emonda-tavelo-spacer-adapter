# Konstruktion

Adapter zwischen dem originalen Trek-Steuersatzdeckel (Émonda SL 6, 2024) und dem Tavelo-Avro-Rise-Cockpit.

**Stand:** Rev. C, 2026-09-29: Prototyp 1 gedruckt und am Rad geprüft, Änderungen eingearbeitet (Abschnitt 6). Prototyp 2 (Rev. C, FDM) ist in Fertigung. Nächster Schritt: dessen Befund in Abschnitt 6 eintragen.

---

## 1. Schnittstellen

| ID | Schnittstelle | Gegenstück | Festlegung |
|---|---|---|---|
| IF-1 | Unterseite ↔ Trek-Deckel | originaler Trek-Deckel, bleibt unverändert | Kontur 60,5 × 39,5 (Spitze 2,5 weiter vorn als oben), zwei Nasen, Neigung α_T |
| IF-2 | Oberseite ↔ Tavelo-Vorbau | Vorbauunterseite (identisch zur Spacer-Sitzfläche) | Kontur 58 × 39,5, zwei Stifte in die Sacklöcher des Vorbaus, Neigung α_V |
| IF-3 | Bohrung ↔ Gabelschaft | Carbonschaft Ø 28,6, seitlich abgeflacht auf 26,75 | Bohrung Ø 30 senkrecht zur Schaftachse, als Langloch 2 nach hinten verlängert (32 × 30), entlang der Schaftachse |
| IF-4 | Leitungsführung | 2 Bremsleitungen (Di2 funkt) | Tavelo-Kanal → Sichel → Öffnung im Trek-Deckel → Rahmen |

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
| Stifte oben (Tavelo) | Ø 3 × 1,85; Abstand 28,75; 42,0 ab Hinterkante (Prototyp 40,5: Adapter saß 1,5 zu weit vorn) | x = −12,0; y = ±14,375 (in der Oberseite) |
| Trek-Nasen | Langloch 7,6 × 2,4 × 1,5; äußerste Punkte 20,25 auseinander, innerste 11,35; Längsausdehnung 7,0 | Mitte x = +20,0; y = ±7,9; 24° zur Längsachse, V-förmig (vorn außen) |
| Taschen für die Nasen | Nase + 0,3 Spiel pro Seite, Tiefe 2,5; vorderes (inneres) Ende zur Bohrung geöffnet (Durchbruch in Taschenbreite) | |
| Höhe | 20 entlang der Schaftachse | senkrecht zur Unterseite: hinten 15,5 / Achse 20,1 / vorn 24,3 |

Die Skizze V2 in `01_Input/` nennt eine Gesamtlänge von 52,2; das war ein Messfehler, richtig sind 58 (13 + ~15 + 30).

Nasenwinkel abgeleitet: aus der Querausdehnung 23,2°, aus der Längsausdehnung 27,8°, beides erfüllt bei 24,0°. Die Maße sind auf ±0,2 konsistent; das Taschenspiel deckt die Unsicherheit ab.

## 4. Winkel und Keil

| Größe | Wert | Quelle |
|---|---|---|
| α_T: Trek-Sitzfläche gegen die Schaftnormale | **17°** | geschätzt (Trek-Stapel im Fahrbetrieb etwa waagerecht, Lenkwinkel ~73°), **am Prototyp 1 bestätigt**: untere Fuge schließt |
| α_V: Tavelo-Sitzfläche gegen die Schaftnormale | **8°** | gemessen: Klemmbohrung 8° nach hinten gekippt bei flach aufliegender Sitzfläche; am Prototyp 1 bestätigt |
| Keil zwischen Unter- und Oberseite | **α_T − α_V ≈ 9°** | hinten dünn, vorn dick |

Gegenprobe α_V: Der Vorbau steht 80° zur Schaftachse und fällt damit relativ zur eigenen Sitzfläche um 2° ab. Am Émonda steigt die Sitzfläche 9° über die Horizontale, der Vorbau 7°. Das ist konsistent. Die gemessene „30-mm-Bohrung" der Tavelo-Spacer ist Spiel (28,6 / cos 8° = 28,9). Der Adapter übernimmt die 30.

Der Lenkwinkel spielt für die Passung keine Rolle. Maßgeblich sind nur die Neigungen der Sitzflächen relativ zur Schaftachse.

## 5. Konstruktionsentscheidungen

| ID | Entscheidung | Begründung |
|---|---|---|
| D-1 | Bohrung Ø 30 senkrecht zur Schaftachse (0,7 Spiel radial zum Schaft Ø 28,6), als Langloch 2 nach hinten verlängert (32 × 30); Vorderkante 15 vor der Achse | Die Lage kommt von den Trek-Nasen unten und den Tavelo-Stiften oben, nicht vom Schaft. Das Langloch gibt dem Vorbau nach hinten Luft. Der Prototyp (Ø 28,9, Kreise parallel zur Unterseite gezeichnet) war senkrecht zur Achse längs nur 27,6 und damit enger als der Schaft. Die Tavelo-Spacer haben ebenfalls 30. Wand zu den Stiften 2,1. Die Nasentaschen sind zur Bohrung geöffnet (D-9). |
| D-2 | Außenwand = Regelfläche zwischen Trek-Kontur (unten) und Tavelo-Kontur (oben) | Beide Fugen schließen bündig, obwohl die Ebenen 9° gegeneinander stehen. |
| D-3 | Bohrung, Sichel und Gelenk entlang der Schaftachse | Das Teil wird entlang des Schafts gefügt, die Leitungen laufen parallel zum Schaft. Sichel und Gelenk sind als Profil parallel zur Unterseite definiert und entlang der Achse geschert, senkrecht zur Achse also längs um cos α_T kürzer; für sie ist das unerheblich. Die Bohrung ist ein echter Zylinder um die Achse (siehe D-1). |
| D-4 | Zweiteilig, Teilung bei y = 0 | Montage um Schaft und Leitungen, ohne die Hydraulik zu öffnen. |
| D-5 | **Gelenk nach Tavelo-Vorbild:** je Teilstelle zwei Zapfen mit Hals in Schlüssellochaufnahmen, unten von A nach B, oben von B nach A. Vorn: Ø 3,2 / Hals 1,6 / Versatz 2,4, bei x = −24,85 (Prototyp −24,1; verschoben für mehr Wand zum Kanal, min. 1,6). Hinten: Ø 4,0 / Hals 2,2 / Versatz 2,9, bei x = +26,0. Spiel 0,2 radial, 0,15 axial, Fuge 0,25 | Die Zapfen sperren quer. Gefügt wird durch Aufschieben von B entlang des Schafts. CAD-Kollisionstest: keine Überschneidung; quer blockiert ab ~0,5 mm; entlang des Schafts frei fügbar. |
| D-6 | Höhe 20 entlang der Schaftachse | ersetzt einen 20-mm-Spacerstapel |
| D-7 | Werkstoff PA12 (MJF) für das Endteil | Das Teil liegt in der Kraftkette der Lagervorspannung und wird warm; kein PLA/PETG. |
| D-8 | Drucklayout: beide Hälften in einer Datei, getrennt, Unterseite auf dem Druckbett | ein Auftrag, keine verschränkten Teile im Druck |
| D-9 | Nasentaschen am vorderen (inneren) Ende zur Bohrung geöffnet: Durchbruch in Taschenbreite (3,0) Richtung Schaftachse, Tiefe wie die Tasche | Durch das Langloch bliebe nur ein Steg von 0,27, der beim Druck oder bei der Montage wegbricht. Offen gibt es keine losen Splitter; die Übergänge zur Bohrung sind stumpfwinklig. Die Nasen werden seitlich und am hinteren Ende geführt. |
| D-10 | Kantenradien: an Ober- und Unterseite Bohrung R 1,0, Leitungskanal R 0,5; innen am Übergang Langloch → Leitungskanal (Kante entlang der Achse) R 2,0 | Sauberes Aussehen, keine scharfen Kanten an den Leitungen. Am Kanal nur R 0,5, weil R 1,0 die Wand zur oberen vorderen Gelenkaufnahme auf 0,64 senkt (mit R 0,5: 1,21). |

## 6. Prototyp 1: Befund und Änderungen

Selbst gedruckt, am Rad montiert (2026-09-29).

| Befund | Ursache | Änderung (Rev. C) |
|---|---|---|
| Winkel oben und unten passen, beide Fugen schließen | – | α_T = 17° und α_V = 8° bestätigt |
| Gelenk passt | – | vorderes Gelenk trotzdem 0,75 nach vorn (x = −24,85): Wand zum Leitungskanal 1,05 → 1,8 |
| Bohrung sehr schwer aufzuziehen, musste aufgefeilt werden | Kreise parallel zur Unterseite gezeichnet, senkrecht zur Achse längs nur 27,6 (Schaft 28,6) | Bohrung als echter Zylinder um die Achse, Ø 30, Langloch 2 nach hinten (D-1) |
| Adapter sitzt 1,5 zu weit vorn: steht vorn über den Vorbau, hinten fehlt Material | Stifte 1,5 zu weit hinten (Skizzenmaß 40,5 ab Hinterkante) | Stifte 42,0 ab Hinterkante (x = −12,0). Merkregel: Die Stifte sind im Vorbau fixiert; Stifte im Adapter nach vorn → Adapter wandert nach hinten |
| Seitlich kein Versatz | – | – |
| Taschen für die Trek-Nasen zu flach | – | Taschentiefe 1,8 → 2,5 |
| Untere Kante vorn muss weiter nach vorn | – | Unterseite vorn 2,5 länger (60,5); Oberseite exakt unverändert, weil dort der Vorbau passgenau aufliegt. Dadurch wird nur die Stirnwand vorn schräger |

## 7. Offene Punkte

| ID | Punkt | Stand |
|---|---|---|
| O-1 | Wand zwischen Bohrungs-Langloch und Nasentaschen nur 0,27 | erledigt: Taschen zur Bohrung geöffnet (D-9) |
| O-2 | Feinschliff | erledigt: vorderes Gelenk verschoben (D-5), Taschen offen (D-9), Kantenradien (D-10) |
| O-3 | Prototyp 2 (Rev. C, FDM) am Rad prüfen, dann Endteil in PA12 (MJF) | Prototyp 2 in Fertigung. Prüfen: Stifte ohne Druck in den Sacklöchern, B ohne Klemmen aufschiebbar, vorn und hinten bündig, Aufziehen ohne Feilen, Fugen dicht |
| O-4 | Idee: Stahlstifte statt gedruckter Stifte (Zylinderstift Ø 3 × 6, ISO 8734, in Bohrung ≈ Ø 2,9 eingepresst; Passmaß ist eine Annahme) | nicht umgesetzt; erst Durchmesser und Tiefe der Sacklöcher im Vorbau messen (bisher ungemessen) |
| O-5 | Idee: Einführfasen 0,3 an den Stiftspitzen, 0,3–0,5 an den Enden der Gelenkzapfen | nicht umgesetzt; erleichtert die Montage |
| O-6 | Idee: Gelenkspiel für MJF auf 0,25–0,3 (`JOINT_CLEAR`) | nicht umgesetzt; Einschätzung, kein Messwert. 0,2 hat im FDM-Prototyp gepasst |
| O-7 | Idee: „A“, „B“ und Revision innen einprägen; Oberfläche des Endteils gefärbt und dampfgeglättet | nicht umgesetzt |

Geprüft und unkritisch (Review Rev. C): Die Vorspannung (angenommen 1–2 kN) drückt den 9°-Keil mit ≈ 16 % nach hinten; Reibung an Ober- und Unterseite (μ ≈ 0,2) hält das allein, dazu Stifte, Nasenflanken und nach 0,7 der Schaft. Flächenpressung ≈ 1–2 MPa auf je ≈ 900 mm². Das Gelenk trägt keine Fahrlasten, jede Hälfte sitzt über eigene Nase und eigenen Stift. Lenk- und Biegemomente laufen über die Vorbauklemmung in den Schaft.

Prüfen nach jeder Änderung: `python 02_CAD/check_adapter.py` (Kollision der Hälften, Bohrungsmaß, Wandstärken).

## 8. Revisionen

| Rev. | Datum | Inhalt |
|---|---|---|
| B.1 | 2026-09-28 | α_V = 8° gemessen → Keil 9°; Höhe entlang der Schaftachse; Regelflächen-Außenwand; Drucklayout. Stand von Prototyp 1 |
| C | 2026-09-29 | Änderungen nach Prototyp 1 (Abschnitt 6); Taschen zur Bohrung geöffnet (D-9); Kantenradien (D-10) |
