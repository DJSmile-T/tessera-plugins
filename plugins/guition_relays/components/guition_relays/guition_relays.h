#pragma once

#include "esphome/core/component.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/smart_display/plugin_api.h"

namespace esphome::guition_relays {

// The plugin: a switch for every relay of the base on the screen's settings page, so a relay can be switched on the
// glass even while Home Assistant is away. The relays are gpio switches of plugin.yaml; Home Assistant sees them as
// switches of the screen.
class GuitionRelays : public Component, public tessera::Plugin {
 public:
  float get_setup_priority() const override { return setup_priority::LATE; }
  bool settings(tessera::SettingsPage &page) override;

  void set_relay(int index, switch_::Switch *relay) { relays_[index] = relay; }

 protected:
  switch_::Switch *relays_[3]{};
};

}  // namespace esphome::guition_relays
