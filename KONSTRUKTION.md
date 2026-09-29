# Konstruktion

Adapter zwischen dem originalen Trek-Steuersatzdeckel (Émonda SL 6, 2024) und dem Tavelo-Avro-Rise-Cockpit.

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
- **x:** Längsachse, **+x nach hinten** (Richtung Oberrohr), Spitze vorn bei x = −28
- **y:** quer; Teilungsebene y = 0, Hälfte A bei y > 0, Hälfte B bei y < 0
- **z:** Normale der Unterseite
- **Schaftachse:** um α_T gegen z nach hinten geneigt

## 3. Maße (bemaßt; Skizze V2 plus Nachmessungen)

| Merkmal | Wert | Im Koordinatensystem |
|---|---|---|
| Kontur oben (Tavelo, in der Oberseite) | 58 × 39,5 | x = −28 … +30; y = ±19,75 |
| Kontur unten (Trek, in der Unterseite) | 60,5 × 39,5: vordere Hälfte nach vorn gestreckt, Spitze 2,5 weiter vorn; hintere Hälfte wie oben | x = −30,5 … +30 |
| Bohrungsmitte → Hinterkante | 30 | |
| vordere Bohrungskante → Spitze | 13,0 | |
| Sichel (Leitungskanal, zur Bohrung offen) | Vorderkante 6,8 hinter der Spitze; Breite außen 22,75 / innen 20,2 | x = −21,2; y = ±11,375 / ±10,1 |
| Stifte oben (Tavelo) | Ø 3 × 1,85; Abstand 28,75; 42,0 ab Hinterkante (Prototyp 40,5: Adapter saß 1,5 zu weit vorn) | x = −12,0; y = ±14,375 (in der Oberseite) |
| Trek-Nasen | Langloch 7,6 × 2,4 × 1,5; äußerste Punkte 20,25 auseinander, innerste 11,35; Längsausdehnung 7,0 | Mitte x = +20,0; y = ±7,9; 24° zur Längsachse, V-förmig (vorn außen) |
| Taschen für die Nasen | Nase + 0,3 Spiel pro Seite, Tiefe 2,5 | |
| Höhe | 20 entlang der Schaftachse | senkrecht zur Unterseite: hinten 15,5 / Achse 20,1 / vorn 24,3 |

Nasenwinkel abgeleitet: aus der Querausdehnung 23,2°, aus der Längsausdehnung 27,8°, beides erfüllt bei 24,0°. Die Maße sind auf ±0,2 konsistent; das Taschenspiel deckt die Unsicherheit ab.

## 4. Winkel und Keil

| Größe | Wert | Quelle |
|---|---|---|
| α_T: Trek-Sitzfläche gegen die Schaftnormale | **17°** | Trek-Stapel im Fahrbetrieb etwa waagerecht, Lenkwinkel ~73°; geschätzt, nicht gemessen |
| α_V: Tavelo-Sitzfläche gegen die Schaftnormale | **8°** | gemessen: Klemmbohrung 8° nach hinten gekippt bei flach aufliegender Sitzfläche |
| Keil zwischen Unter- und Oberseite | **α_T − α_V ≈ 9°** | hinten dünn, vorn dick |

Gegenprobe α_V: Der Vorbau steht 80° zur Schaftachse und fällt damit relativ zur eigenen Sitzfläche um 2° ab. Am Émonda steigt die Sitzfläche 9° über die Horizontale, der Vorbau 7°. Das ist konsistent. Die gemessene „30-mm-Bohrung" der Tavelo-Spacer ist Spiel (28,6 / cos 8° = 28,9). Der Adapter übernimmt die 30.

Der Lenkwinkel spielt für die Passung keine Rolle. Maßgeblich sind nur die Neigungen der Sitzflächen relativ zur Schaftachse.

## 5. Konstruktionsentscheidungen

| ID | Entscheidung | Begründung |
|---|---|---|
| D-1 | Bohrung Ø 30 senkrecht zur Schaftachse (0,7 Spiel radial zum Schaft Ø 28,6), als Langloch 2 nach hinten verlängert (32 × 30); Vorderkante 15 vor der Achse | Die Lage kommt von den Trek-Nasen unten und den Tavelo-Stiften oben, nicht vom Schaft. Das Langloch gibt dem Vorbau nach hinten Luft. Der Prototyp (Ø 28,9, Kreise parallel zur Unterseite gezeichnet) war senkrecht zur Achse längs nur 27,6 und damit enger als der Schaft. Die Tavelo-Spacer haben ebenfalls 30. Wand zu den Stiften 2,1; zu den Nasentaschen nur 0,3 (noch offen). |
| D-2 | Außenwand = Regelfläche zwischen Trek-Kontur (unten) und Tavelo-Kontur (oben) | Beide Fugen schließen bündig, obwohl die Ebenen 9° gegeneinander stehen. |
| D-3 | Bohrung, Sichel und Gelenk entlang der Schaftachse | Das Teil wird entlang des Schafts gefügt, die Leitungen laufen parallel zum Schaft. |
| D-4 | Zweiteilig, Teilung bei y = 0 | Montage um Schaft und Leitungen, ohne die Hydraulik zu öffnen. |
| D-5 | **Gelenk nach Tavelo-Vorbild:** je Teilstelle zwei Zapfen mit Hals in Schlüssellochaufnahmen, unten von A nach B, oben von B nach A. Vorn: Ø 3,2 / Hals 1,6 / Versatz 2,4, bei x = −24,85 (Prototyp −24,1; verschoben für mehr Wand zum Kanal, min. 1,6). Hinten: Ø 4,0 / Hals 2,2 / Versatz 2,9, bei x = +26,0. Spiel 0,2 radial, 0,15 axial, Fuge 0,25 | Die Zapfen sperren quer. Gefügt wird durch Aufschieben von B entlang des Schafts. CAD-Kollisionstest: keine Überschneidung; quer blockiert ab ~0,5 mm; entlang des Schafts frei fügbar. |
| D-6 | Höhe 20 entlang der Schaftachse | ersetzt einen 20-mm-Spacerstapel |
| D-7 | Werkstoff PA12 (MJF) für das Endteil | Das Teil liegt in der Kraftkette der Lagervorspannung und wird warm; kein PLA/PETG. |
| D-8 | Drucklayout: beide Hälften in einer Datei, getrennt, Unterseite auf dem Druckbett | ein Auftrag, keine verschränkten Teile im Druck |
