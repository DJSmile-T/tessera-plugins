#include "guition_relays.h"

namespace esphome::guition_relays {

bool GuitionRelays::settings(tessera::SettingsPage &page) {
  static const char *const NAMES[] = {"relay_1", "relay_2", "relay_3"};
  page.icon = "\U000F0521";
  for (int i = 0; i < 3; i++) {
    switch_::Switch *relay = relays_[i];
    if (relay == nullptr) continue;
    page.toggle(text(NAMES[i]), [relay] { return relay->state; },
                [relay](bool on) { on ? relay->turn_on() : relay->turn_off(); });
  }
  return true;
}

}  // namespace esphome::guition_relays
