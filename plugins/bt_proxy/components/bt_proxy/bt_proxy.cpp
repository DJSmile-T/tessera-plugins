#include "bt_proxy.h"

namespace esphome::bt_proxy {

bool BtProxy::settings(tessera::SettingsPage &page) {
  if (proxy_on_ == nullptr) return false;
  page.icon = "\U000F00AF";  // bluetooth
  switch_::Switch *proxy_on = proxy_on_;
  page.toggle(text("proxy"), [proxy_on] { return proxy_on->state; },
              [proxy_on](bool on) { on ? proxy_on->turn_on() : proxy_on->turn_off(); });
  return true;
}

}  // namespace esphome::bt_proxy
