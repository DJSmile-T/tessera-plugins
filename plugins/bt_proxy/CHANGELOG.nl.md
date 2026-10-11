# Wijzigingen

## 0.2.0 - 2026-10-11
- De firmware-update van de wifichip komt mee met de plugin (**Update van de wifichip**, standaard aan): Home Assistant toont hem bij het apparaat van het scherm, en jij drukt op Installeren. Bluetooth vraagt een recente; veel schermen komen met een te oude.
- **Bluetooth status** zegt wat de proxy doet, in Home Assistant en op de instellingenpagina van het scherm: luistert, uit, start op, of dat de wifichip zijn update nodig heeft.
- De update in de Override YAML gehad? Haal dat blok eerst weg; de entiteit houdt zijn naam.

## 0.1.0 - 2026-10-11
- Eerste versie: de Bluetooth-proxy van ESPHome op elk scherm met een ESP32-P4, met een instelling om hem zonder opnieuw bouwen uit te zetten.
- Hij deelt de radio met wifi: plaatjes en camerabeelden kunnen trager zijn zolang hij draait. Lees "Voordat je hem toevoegt" in de README.
- Een Bluetooth-proxy in de Override YAML gehad? Haal eerst de blokken `esp32_ble_tracker:` en `bluetooth_proxy:` weg.
