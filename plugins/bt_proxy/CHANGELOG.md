# Changelog

## 0.2.0 - 2026-10-11
- The Wi-Fi chip's firmware update comes with the plugin (**Wi-Fi chip update**, ticked by default): Home Assistant shows it on the screen's device, and you press Install. Bluetooth needs a recent one; many screens come with one too old.
- **Bluetooth status** says what the proxy does, in Home Assistant and on the screen's settings page: listening, off, starting, or that the Wi-Fi chip needs its update.
- Had the update in the Override YAML? Remove that block first; the entity keeps its name.

## 0.1.0 - 2026-10-11
- First version: ESPHome's Bluetooth proxy on every screen with an ESP32-P4, with a setting to turn it off without a build.
- It shares the radio with Wi-Fi: pictures and camera streams can be slower while it runs. Read "Before you add it" in the README.
- Had a Bluetooth proxy in the Override YAML? Remove its `esp32_ble_tracker:` and `bluetooth_proxy:` blocks first.
