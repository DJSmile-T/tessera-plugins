# Bluetooth proxy

Turns the screen into a Bluetooth proxy for Home Assistant, the same one a ready-made ESPHome Bluetooth proxy runs.
Home Assistant then hears Bluetooth devices near the screen (thermometers, plant sensors, tags for presence with
[Bermuda](https://github.com/agittins/bermuda)) and can connect to some of them through it (a lock, a light), up to
three at a time.

## Before you add it: Wi-Fi

The screen does Wi-Fi and Bluetooth with one radio, so every moment it listens for Bluetooth is a moment without
Wi-Fi. The plugin listens the way ESPHome's own Wi-Fi proxies do, a short slice of time at a steady pace, but the
screen still has less Wi-Fi than before:

- Pictures, covers and camera streams can load more slowly. One tester saw a camera stream run clearly smoother with
  the proxy off.
- On weak Wi-Fi the screen can react more slowly to Home Assistant, or drop its connection more often.

Turn the proxy off at any time with the setting **Bluetooth proxy** (below), without a build. When the screen shows
camera streams, or hangs on the edge of your Wi-Fi, a separate ESP32 as a Bluetooth proxy is the better choice: it costs
a few euros and you can put it where the reception is best.

## Which screens

Every screen with an ESP32-P4 (the Guition P4 screens, the Waveshare P4 86, the M5Stack Tab5, the reTerminal D1001,
the CrowPanel 10.1). The P4 runs Bluetooth through the ESP32-C6 beside it, which also does its Wi-Fi, and has the
memory to spare. The app only offers the plugin on those screens.

Not on an ESP32-S3 with an RGB panel (the 4-inch Guition, the Waveshare 4.3, 5 and 7-inch, and their kind): Bluetooth
needs memory inside the chip that the panel and Wi-Fi already use, and such a screen stops connecting. Not on the CYD
and other 4 MB screens either: there is no room for it.

## What you need

- A screen with an ESP32-P4.
- A recent firmware on its ESP32-C6. The C6 often comes with a firmware too old for Bluetooth (a reTerminal D1001 came
  with 2.3.2); see "Updating the C6" below. With the old firmware the screen works as before and Bluetooth stays off.

## Set up

1. In Tessera, open **Plugins**, choose **Bluetooth proxy** and tick your screen.
2. Add it. The screen builds once.
3. In Home Assistant, open **Settings**, **Devices & services**, **Bluetooth**: the screen shows up as a proxy, named
   after the screen and the Bluetooth address of its C6 (not the Wi-Fi address of the screen), and devices it hears
   appear as Home Assistant finds them.
4. No devices after a few minutes? Look at the screen's log in ESPHome. `BT controller init failed; co-processor
   firmware ... may lack BT support` means the C6 firmware is too old: update it (below). Home Assistant may list the
   proxy anyway, but it does not scan until the C6 is updated.

## The setting

**Bluetooth proxy** turns Bluetooth on and off. It is in Home Assistant on the screen's device, in the plugin's details
on the screen's Plugins tab in Tessera, and on the screen itself: hold the top bar, then **Settings**, **Plugins**,
**Bluetooth**. Off gives the radio to Wi-Fi alone; the screen keeps it off across a restart until you turn it on.

## Updating the C6

The ESP32-C6 has a firmware of its own, and ESPHome publishes newer ones. Tessera never updates it by itself: an update
that goes wrong leaves the C6 starting over and over, and only its download mode brings it back, which on some screens
means opening the case. So it is a step you take on purpose, once, for your own screen:

1. In Tessera, open the screen, then **More**, **Override YAML**, and add:

   ```yaml
   http_request:

   update:
     - platform: esp32_hosted
       type: http
       name: "Wi-Fi co-processor firmware"
       source: https://esphome.github.io/esp-hosted-firmware/manifest/esp32c6.json
   ```

2. Save and let the screen build.
3. In Home Assistant, the screen's device now has **Wi-Fi co-processor firmware**. It shows the version on the C6 and
   the newest one. Press **Install** when you are ready, and leave the screen powered until it is done. The screen
   restarts afterwards, and Bluetooth starts.
4. Afterwards you may remove the block again, or keep it to hear of newer versions (it checks every six hours and
   installs only when you press Install).

## Good to know

- It adds about 370 KB to the firmware. Every P4 screen has room for that.
- The proxy follows ESPHome's own: what Home Assistant does with it is in the
  [ESPHome Bluetooth proxy docs](https://esphome.io/components/bluetooth_proxy/).
- Added a Bluetooth proxy through the screen's **Override YAML** before? Remove those blocks (`esp32_ble_tracker:`,
  `bluetooth_proxy:`) first, or the build finds them twice. The C6 update block may stay.
