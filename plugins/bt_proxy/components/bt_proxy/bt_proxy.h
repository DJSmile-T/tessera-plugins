#pragma once

#include <string>

#include "esphome/core/component.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/smart_display/plugin_api.h"

namespace esphome::bt_proxy {

// The plugin: the Bluetooth proxy's switch and status on the screen's settings page, so Bluetooth can be turned off on
// the glass when the Wi-Fi needs the radio, and a person sees why it does not listen. The proxy is ESPHome's own; the
// switch and the status are a template switch and text sensor of plugin.yaml, which Home Assistant shows as well.
class BtProxy : public Component, public tessera::Plugin {
 public:
  float get_setup_priority() const override { return setup_priority::LATE; }
  void on_ready() override;
  void on_interval(uint32_t now_ms) override;
  bool settings(tessera::SettingsPage &page) override;

  void set_proxy_on(switch_::Switch *proxy_on) { proxy_on_ = proxy_on; }
  void set_status(text_sensor::TextSensor *status) { status_ = status; }

 protected:
  // The key of the screen's text for what Bluetooth does now: status_on, status_off, status_old or status_starting.
  const char *state_() const;
  void publish_();

  switch_::Switch *proxy_on_{nullptr};
  text_sensor::TextSensor *status_{nullptr};
  const char *published_{nullptr};
  uint32_t last_ms_{0};
};

}  // namespace esphome::bt_proxy
