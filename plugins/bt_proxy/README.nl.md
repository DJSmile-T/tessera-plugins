# Bluetooth-proxy

Maakt van het scherm een Bluetooth-proxy voor Home Assistant, dezelfde die een kant-en-klare ESPHome Bluetooth-proxy
draait. Home Assistant hoort dan Bluetooth-apparaten bij het scherm (thermometers, plantsensoren, tags voor
aanwezigheid met [Bermuda](https://github.com/agittins/bermuda)) en kan via het scherm met sommige verbinden (een slot,
een lamp), tot drie tegelijk.

## Voordat je hem toevoegt: wifi

Het scherm doet wifi en Bluetooth met één radio, dus elk moment dat het naar Bluetooth luistert is een moment zonder
wifi. De plugin luistert zoals de wifi-proxies van ESPHome zelf, een kort stukje tijd in een vast ritme, maar het scherm
heeft toch minder wifi dan eerst:

- Plaatjes, hoesjes en camerabeelden kunnen langzamer laden. Een tester zag een camerabeeld duidelijk vlotter lopen
  met de proxy uit.
- Bij zwakke wifi kan het scherm trager reageren op Home Assistant, of vaker de verbinding kwijtraken.

Zet de proxy op elk moment uit met de instelling **Bluetooth-proxy** (hieronder), zonder opnieuw bouwen. Toont het
scherm camerabeelden, of hangt het aan de rand van je wifi, dan is een losse ESP32 als Bluetooth-proxy de betere keus:
die kost een paar euro en zet je waar de ontvangst het best is.

## Welke schermen

Elk scherm met een ESP32-P4 (de Guition P4-schermen, het Waveshare P4 86, de M5Stack Tab5, de reTerminal D1001, de
CrowPanel 10.1). De P4 doet Bluetooth via de ESP32-C6 ernaast, die ook de wifi doet, en heeft het geheugen over. De app
biedt de plugin alleen op die schermen aan.

Niet op een ESP32-S3 met een RGB-paneel (de Guition 4-inch, de Waveshare 4,3, 5 en 7-inch en hun soort): Bluetooth heeft
geheugen in de chip nodig dat het paneel en wifi al gebruiken, en zo'n scherm maakt dan geen verbinding meer. Ook niet
op de CYD en andere schermen met 4 MB: daar is geen ruimte voor.

## Wat je nodig hebt

- Een scherm met een ESP32-P4.
- Een recente firmware op de ESP32-C6. De C6 komt vaak met een firmware die te oud is voor Bluetooth (een reTerminal
  D1001 kwam met 2.3.2); zie "De C6 bijwerken" hieronder. Met de oude firmware werkt het scherm zoals altijd en blijft
  Bluetooth uit.

## Instellen

1. Open in Tessera **Plugins**, kies **Bluetooth-proxy** en vink je scherm aan.
2. Voeg hem toe. Het scherm bouwt één keer.
3. Open in Home Assistant **Instellingen**, **Apparaten & diensten**, **Bluetooth**: het scherm staat er als proxy,
   genoemd naar het scherm en het Bluetooth-adres van zijn C6 (niet het wifi-adres van het scherm), en apparaten die
   het hoort verschijnen zodra Home Assistant ze vindt.
4. Na een paar minuten geen apparaten? Kijk in het log van het scherm in ESPHome. `BT controller init failed;
   co-processor firmware ... may lack BT support` betekent dat de C6-firmware te oud is: werk hem bij (hieronder). Home
   Assistant kan de proxy dan toch tonen, maar hij scant pas na de update van de C6.

## De instelling

**Bluetooth-proxy** zet Bluetooth aan en uit. Hij staat in Home Assistant bij het apparaat van het scherm, in de details
van de plugin op het tabblad Plugins van het scherm in Tessera, en op het scherm zelf: houd de bovenbalk vast, dan
**Instellingen**, **Plugins**, **Bluetooth**. Uit geeft de radio alleen aan wifi; het scherm houdt hem ook na een
herstart uit tot je hem weer aanzet.

## De C6 bijwerken

De ESP32-C6 heeft een eigen firmware, en ESPHome brengt nieuwere uit. Tessera werkt hem nooit vanzelf bij: een update
die misgaat laat de C6 steeds opnieuw starten, en alleen zijn downloadmodus haalt hem terug, wat bij sommige schermen
betekent dat de behuizing open moet. Het is dus een stap die je bewust zet, één keer, voor je eigen scherm:

1. Open in Tessera het scherm, dan **Meer**, **Override YAML**, en voeg toe:

   ```yaml
   http_request:

   update:
     - platform: esp32_hosted
       type: http
       name: "Wi-Fi co-processor firmware"
       source: https://esphome.github.io/esp-hosted-firmware/manifest/esp32c6.json
   ```

2. Sla op en laat het scherm bouwen.
3. In Home Assistant heeft het apparaat van het scherm nu **Wi-Fi co-processor firmware**. Die toont de versie op de C6
   en de nieuwste. Druk op **Installeren** als je zover bent, en laat het scherm aan tot hij klaar is. Het scherm
   herstart daarna, en Bluetooth start.
4. Daarna mag het blok er weer uit, of laat het staan om van nieuwere versies te horen (hij kijkt elke zes uur en
   installeert pas als je op Installeren drukt).

## Goed om te weten

- Hij voegt ongeveer 370 KB toe aan de firmware. Elk P4-scherm heeft daar ruimte voor.
- De proxy is die van ESPHome zelf: wat Home Assistant ermee doet staat in de
  [ESPHome-documentatie over de Bluetooth-proxy](https://esphome.io/components/bluetooth_proxy/).
- Eerder een Bluetooth-proxy toegevoegd via de **Override YAML** van het scherm? Haal die blokken (`esp32_ble_tracker:`,
  `bluetooth_proxy:`) eerst weg, anders vindt de build ze twee keer. Het blok voor de C6-update mag blijven.
