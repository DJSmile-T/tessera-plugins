# Changelog

## 0.1.0 - 2026-10-11
- First version: ESPHome's Bluetooth proxy on every screen with an ESP32-P4, with a setting to turn it off without a build.
- It shares the radio with Wi-Fi: pictures and camera streams can be slower while it runs. Read "Before you add it" in the README.
- Had a Bluetooth proxy in the Override YAML? Remove its `esp32_ble_tracker:` and `bluetooth_proxy:` blocks first.
