#pragma once

#include "esphome/core/component.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/smart_display/plugin_api.h"

namespace esphome::bt_proxy {

// The plugin: the Bluetooth proxy's switch on the screen's settings page, so Bluetooth can be turned off on the glass
// when the Wi-Fi needs the radio. The proxy is ESPHome's own; the switch is a template switch of plugin.yaml, which
// Home Assistant and the Tessera app show as well.
class BtProxy : public Component, public tessera::Plugin {
 public:
  float get_setup_priority() const override { return setup_priority::LATE; }
  bool settings(tessera::SettingsPage &page) override;

  void set_proxy_on(switch_::Switch *proxy_on) { proxy_on_ = proxy_on; }

 protected:
  switch_::Switch *proxy_on_{nullptr};
};

}  // namespace esphome::bt_proxy
