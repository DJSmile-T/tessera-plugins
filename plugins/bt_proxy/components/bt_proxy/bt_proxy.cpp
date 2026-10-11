#include "bt_proxy.h"

#include "esphome/components/esp32_ble/ble.h"

namespace esphome::bt_proxy {

const char *BtProxy::state_() const {
  esp32_ble::ESP32BLE *ble = esp32_ble::global_ble;
  // ESPHome marks its Bluetooth failed when the C6 cannot run it: its firmware is too old for Bluetooth.
  if (ble == nullptr || ble->is_failed()) return "status_old";
  if (proxy_on_ != nullptr && !proxy_on_->state) return "status_off";
  return ble->is_active() ? "status_on" : "status_starting";
}

void BtProxy::publish_() {
  const char *state = state_();
  if (state == published_ || status_ == nullptr) return;
  published_ = state;
  status_->publish_state(text(state));
}

void BtProxy::on_ready() { publish_(); }

void BtProxy::on_interval(uint32_t now_ms) {
  if (now_ms - last_ms_ < 1000) return;
  last_ms_ = now_ms;
  publish_();
}

bool BtProxy::settings(tessera::SettingsPage &page) {
  if (proxy_on_ == nullptr) return false;
  page.icon = "\U000F00AF";  // bluetooth
  switch_::Switch *proxy_on = proxy_on_;
  page.toggle(text("proxy"), [proxy_on] { return proxy_on->state; },
              [proxy_on](bool on) { on ? proxy_on->turn_on() : proxy_on->turn_off(); });
  page.info(text("status"), [this] { return std::string(text(state_())); });
  return true;
}

}  // namespace esphome::bt_proxy
