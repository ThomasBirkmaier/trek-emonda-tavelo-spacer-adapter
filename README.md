# Émonda × Tavelo Spacer-Adapter

Zweiteiliger, 3D-gedruckter Adapter, mit dem ein **Tavelo Avro Rise** (integriertes Cockpit) auf einem **Trek Émonda SL 6 (2024)** sitzt. Der originale Trek-Steuersatzdeckel bleibt unverändert.

![Schnitte](03_Renderings/Adapter_H20_Schnitte.png)

## Kurzbeschreibung

- Unterseite passend zum Trek-Deckel (Neigung α_T ≈ 17°, zwei Nasen), Oberseite passend zur Tavelo-Vorbauunterseite (Neigung α_V = 8°, zwei Stifte Ø 3) → **Keil ≈ 9°**, hinten dünn, vorn dick
- Höhe 20 mm entlang der Schaftachse, Bohrung Ø 28,9 für den 28,6er-Schaft
- Leitungskanal („Sichel") vor dem Schaft für die beiden Bremsleitungen
- zwei Hälften mit Gelenk nach Tavelo-Vorbild: montierbar, ohne die Hydraulik zu öffnen

Alle Maße, Winkel, Entscheidungen und offenen Punkte: **[00_Anforderungen.md](00_Anforderungen.md)**

## Struktur

| Ordner | Inhalt |
|---|---|
| `00_Anforderungen.md` | Schnittstellen, Maße, Winkel, Entscheidungen, offene Punkte |
| `01_Input/` | Skizze, Herstellerzeichnung und Fotos, die in das Modell eingeflossen sind |
| `02_CAD/adapter.py` | parametrisches CadQuery-Modell (einzige Quelle der Geometrie) |
| `02_CAD/render_*.py` | Renderings |
| `02_CAD/out/` | Exporte: `Adapter_*` = zusammengebaut; `DRUCK_*` = druckfertig (beide Hälften getrennt in einer Datei) |
| `03_Renderings/` | Schnitte, Iso-Ansicht, Drucklayout |
| `04_Fertigung/` | Druckaufträge mit Material, Passungen, Prüf- und Montageanleitung |

## Neu erzeugen

```bash
pip install -r requirements.txt
python 02_CAD/adapter.py          # Exporte nach 02_CAD/out
python 02_CAD/render_adapter.py   # Renderings Adapter
python 02_CAD/render_lehrkeil.py 17
```

Die wichtigsten Parameter stehen oben in `02_CAD/adapter.py`: `ALPHA_TREK`, `ALPHA_TAVELO`, `HEIGHT`, `JOINT_CLEAR`. Der Winkel steht im Dateinamen der Exporte (`..._T17_V8`).

## Status

- [x] Geometrie Rev. B.1; Prototyp bei Craftcloud in Auftrag (PA12 MJF, α_T = 17° vorläufig)
- [ ] α_T mit den Lehrkeilen bestätigen (15–19°), bei Abweichung neu exportieren
- [ ] Testmontage: Gelenk, beide Fugen gegen Licht, Vorspannung
