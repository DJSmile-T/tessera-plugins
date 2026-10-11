# Guition-relais

Het Guition 4-inch scherm (ESP32-S3-4848S040) wordt ook verkocht op een inbouwdoos op netspanning met een of drie
relais. Deze plugin laat die relais werken: elk relais is een schakelaar van het scherm in Home Assistant, klaar voor
een tegel of een automatisering, en staat op de instellingenpagina van het scherm zelf.

## Wat je nodig hebt

- Een Guition 4-inch scherm op een doos met een of drie relais. Het scherm zonder doos, of op een doos zonder relais,
  heeft niets dat deze plugin kan schakelen.

## Instellen

1. Open in Tessera **Plugins**, kies **Guition-relais** en vink je scherm aan.
2. Doos met drie relais? Vink **Drie relais** aan voor dat scherm. Laat het uit voor een doos met een.
3. Voeg het toe. Het scherm wordt een keer gebouwd.
4. In Home Assistant heeft het apparaat van het scherm nu **Relay 1** (en **Relay 2** en **Relay 3**):
   `switch.<scherm>_relay_1` enzovoort. Geef ze in Home Assistant de naam van wat ze schakelen, zoals "Plafondlamp".
5. Zet in de Layout van Tessera een relais op een tegel, zoals elke andere schakelaar.

Later een andere doos? Open de details van de plugin op het tabblad Plugins van het scherm, vink **Drie relais** aan of
uit en kies **Opslaan en bouwen**.

## Op het scherm

Houd de bovenbalk vast, dan **Instellingen**, **Plugins**, **Relais**: een schakelaar per relais. Die schakelen het
relais op het scherm zelf, dus ze werken ook als Home Assistant weg is. Een tegel schakelt via Home Assistant: zolang
Home Assistant onbereikbaar is houden de relais hun stand, maar kan een tegel ze niet veranderen.

## Goed om te weten

- De relais zitten op GPIO40 (relais 1), GPIO2 (relais 2) en GPIO1 (relais 3), de pinnen van de apparaatpagina van
  ESPHome voor dit bord. Ze zijn active-high, wat een doos met drie relais bevestigde.
- Elk relais houdt zijn stand over een herstart, en staat de allereerste keer uit.
- De relais eerder via de **Override YAML** van het scherm toegevoegd? Haal dat `switch:`-blok eerst weg: de plugin
  gebruikt dezelfde pinnen en dezelfde namen, anders vindt de build elke pin twee keer. Door dezelfde namen houdt Home
  Assistant de entiteiten, hun namen en je automatiseringen.
- Nog niet getest op een doos met een relais. Doet de jouwe iets anders, meld het dan in een issue.

## Veiligheid

De doos werkt op netspanning. Laat hem aansluiten door iemand die daarvoor bevoegd is, en controleer het vermogen van
het relais tegen wat je erop aansluit.
