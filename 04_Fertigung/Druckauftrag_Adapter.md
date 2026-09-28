# Druckauftrag Adapter (Rev. B.1)

**Datei:** `02_CAD/out/DRUCK_Adapter_H20_T17_V8.stl` (alternativ `.3mf` oder `.step`)
- enthält **beide Hälften** als getrennte Körper, 6,2 mm Abstand, nicht verschränkt
- Unterseite (Trek-Auflage) liegt auf z = 0, Bauraum 63,5 × 55,6 × 23,5 mm
- Volumen gesamt ≈ 19,2 cm³ (A ≈ 9,6 / B ≈ 9,6)
- Menge: **1×** (ein Adapter = beide Hälften)

**Hinweis zum Winkel:** Der Prototyp ist mit α_T = 17° bestellt (vorläufiger Wert). Ergeben die Lehrkeile einen anderen Wert,
im Modell `ALPHA_TREK` ändern und neu exportieren; der Dateiname trägt den Winkel (`T17`).

## Verfahren und Material (Craftcloud)

| Zweck | Verfahren | Material | Anmerkung |
|---|---|---|---|
| **Endteil** | MJF (HP Multi Jet Fusion) | **PA12**, schwarz gefärbt | zäh, temperaturfest, maßhaltig etwa ±0,3 mm |
| Prüfteil (optional, günstiger) | SLA | Standard- oder Tough-Resin | maßhaltiger (±0,1), aber spröder; nur für Passprobe, nicht fahren |

- **Nicht** FDM/PLA/PETG für das Endteil (Kraftkette Lagervorspannung, Wärme, Kriechen).
- Ausrichtung beim Drucken: bei MJF unkritisch. Bei SLA den Anbieter bitten, Stützen **nicht** auf Unter- und Oberseite zu setzen (Sitzflächen).

## Passungen im Modell

| Stelle | Spiel | Bewertung für MJF |
|---|---|---|
| Bohrung zum Schaft | 0,15 radial | ok, Teil klemmt nicht |
| Gelenk-Zapfen in Aufnahme | 0,2 radial | eher knapp; falls es klemmt, Zapfen leicht nachschleifen |
| Nasentaschen | 0,3 pro Seite | ok |
| Stifte Ø3 in Vorbau-Sacklöcher | Nennmaß | bei Bedarf leicht anschleifen |

Dünnste Wand: ~1,0 mm am vorderen Gelenk (Mindestwand MJF ≈ 0,8 mm).

## Montage

1. Vorbau ab, Trek-Deckel bleibt, Leitungen bleiben dran.
2. Hälfte **A** (Zapfen unten) von der Seite an Schaft und Leitungen legen, Nase in die Tasche.
3. Hälfte **B** (Zapfen oben) seitlich ansetzen und **entlang des Schafts** von oben einschieben, bis sie auf dem Deckel aufsitzt.
4. Tavelo-Vorbau aufsetzen, Stifte in die Sacklöcher, Vorspannung wie gewohnt einstellen.
5. Beide Fugen gegen Licht prüfen: Trek-Deckel/Adapter und Adapter/Vorbau.
