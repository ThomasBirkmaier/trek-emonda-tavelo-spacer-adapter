# Trek Émonda × Tavelo Avro Rise – Spacer-Adapter

![Adapter, beide Druckhälften](03_Renderings/Hero.png)

Zweiteiliger, 3D-gedruckter Adapter, mit dem ein integriertes **Tavelo Avro Rise**-Cockpit auf einem **Trek Émonda SL 6 (2024)** sitzt. Der originale Trek-Steuersatzdeckel bleibt unverändert, die Bremsleitungen laufen innen, und für die Montage muss die Hydraulik nicht geöffnet werden.

Das Modell ist parametrisch (Python/CadQuery). Wer einen anderen Rahmen oder andere Winkel hat, ändert ein paar Zahlen und exportiert neu.

## Auf einen Blick

| | |
|---|---|
| Unterseite | passt auf den Trek-Deckel: Neigung α_T ≈ 17°, zwei Nasen rasten ein |
| Oberseite | passt unter den Tavelo-Vorbau: Neigung α_V = 8°, zwei Stifte Ø 3 greifen in die Sacklöcher |
| Keil | ≈ 9°, hinten dünn (15,5 mm), vorn dick (24,3 mm) |
| Höhe | 20 mm entlang der Schaftachse (ersetzt einen 20-mm-Spacerstapel) |
| Schaft | Ø 28,6 (seitlich abgeflacht auf 26,75), Bohrung Ø 28,9 |
| Leitungen | Kanal vor dem Schaft für zwei Bremsleitungen (Di2, funkend) |
| Teilung | zwei Hälften mit Gelenk nach Tavelo-Vorbild, werden entlang des Schafts zusammengeschoben |
| Werkstoff | PA12, MJF-Druck |

## Schnellstart

### Ich will nur drucken

1. Datei **`02_CAD/out/DRUCK_Adapter_H20_T17_V8.stl`** (oder `.3mf`/`.step`) bei einem Druckdienst hochladen, zum Beispiel Craftcloud. Die Datei enthält beide Hälften, getrennt gelegt; die Menge ist 1.
2. Verfahren **MJF**, Material **PA12**, Farbe schwarz. Kein FDM/PLA/PETG: Das Teil liegt in der Kraftkette der Lagervorspannung.
3. Optional vorab die **Lehrkeile** (`DRUCK_Lehrkeil_15…19deg`) drucken, um den Trek-Winkel am eigenen Rad zu prüfen. Kosten: wenige Euro, SLA-Resin reicht.

Details zu Material, Passungen und Prüfung: [`04_Fertigung/`](04_Fertigung/)

### Ich will das Modell anpassen

Voraussetzung: Python 3.10–3.12.

```bash
git clone https://github.com/ThomasBirkmaier/trek-emonda-tavelo-spacer-adapter.git
cd trek-emonda-tavelo-spacer-adapter
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python 02_CAD/adapter.py             # exportiert Adapter + Lehrkeile nach 02_CAD/out
python 02_CAD/render_adapter.py      # Schnitte, Iso-Ansicht
python 02_CAD/render_lehrkeil.py 17  # Rendering eines Lehrkeils
```

Die Parameter stehen oben in [`02_CAD/adapter.py`](02_CAD/adapter.py):

| Parameter | Bedeutung | Aktuell |
|---|---|---|
| `ALPHA_TREK` | Neigung der Trek-Sitzfläche gegen die Schaftnormale | 17,0° (vorläufig) |
| `ALPHA_TAVELO` | Neigung der Tavelo-Sitzfläche gegen die Schaftnormale | 8,0° (gemessen) |
| `HEIGHT` | Höhe entlang der Schaftachse | 20 mm |
| `JOINT_CLEAR` | radiales Spiel im Gelenk | 0,2 mm (bei engen Toleranzen 0,3) |
| `BORE_CLEAR` | radiales Spiel Bohrung/Schaft | 0,15 mm |
| `outline_wire_pts()`, `NOSE_*`, `PIN_*` | Kontur, Nasen, Stifte | laut Skizze V2 |

Die Winkel stehen im Dateinamen der Exporte (`..._T17_V8`), damit man sieht, welche Version man druckt.

## Montage

1. Vorbau abnehmen; der Trek-Deckel bleibt, die Leitungen bleiben angeschlossen.
2. Hälfte **A** (Zapfen unten) seitlich an Schaft und Leitungen legen, die Nase sitzt in der Tasche.
3. Hälfte **B** (Zapfen oben) seitlich ansetzen und **entlang des Schafts** von oben einschieben, bis sie aufsitzt.
4. Tavelo-Vorbau aufsetzen, die Stifte rasten in die Sacklöcher, Vorspannung wie gewohnt einstellen.
5. Beide Fugen gegen Licht prüfen: Trek-Deckel ↔ Adapter und Adapter ↔ Vorbau.

## Repository-Struktur

| Pfad | Inhalt |
|---|---|
| [`00_Anforderungen.md`](00_Anforderungen.md) | Schnittstellen, Maße, Winkel, Konstruktionsentscheidungen, offene Punkte |
| `01_Input/` | Skizze, Herstellerzeichnung und Fotos, die ins Modell eingeflossen sind |
| `02_CAD/adapter.py` | parametrisches Modell, einzige Quelle der Geometrie |
| `02_CAD/out/` | `Adapter_*` = zusammengebaut (Ansicht); `DRUCK_*` = druckfertig |
| `03_Renderings/` | Aufmacherbild, Schnitte, Iso-Ansicht, Drucklayout |
| `04_Fertigung/` | Druckaufträge mit Material, Passungen, Prüf- und Montageanleitung |

## Status

- [x] Geometrie Rev. B.1; Prototyp in Fertigung (PA12 MJF, α_T = 17° vorläufig)
- [ ] α_T mit den Lehrkeilen bestätigen, bei Abweichung neu exportieren
- [ ] Testmontage: Gelenk, beide Fugen, Vorspannung, Probefahrt auf der Rolle

![Schnitte](03_Renderings/Adapter_H20_Schnitte.png)

## Hinweis zur Sicherheit

Der Adapter sitzt am Steuersatz und damit an einem sicherheitsrelevanten Bauteil. Er ist ein privates Eigenbauprojekt, nicht vom Hersteller freigegeben und bisher nur als Prototyp erprobt. Maße und Winkel vor dem Druck am eigenen Rad prüfen. Nutzung auf eigene Verantwortung.

## Lizenz

[WTFPL](LICENSE): Jeder darf damit machen, was er will. Ohne jede Gewährleistung, siehe Hinweis zur Sicherheit.
