"""Bluetooth proxy: the switch of plugin.yaml on the screen's own settings page.

The proxy itself is ESPHome's (esp32_ble_tracker and bluetooth_proxy in plugin.yaml); this component only knows the
switch, so it can be turned off and on on the glass. register_plugin() takes the id, version and the screen's texts
from the manifest and translations/.
"""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import smart_display, switch
from esphome.const import CONF_ID

DEPENDENCIES = ["smart_display", "switch", "bluetooth_proxy"]

CONF_PROXY_ON = "proxy_on"

bt_proxy_ns = cg.esphome_ns.namespace("bt_proxy")
BtProxy = bt_proxy_ns.class_("BtProxy", cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(BtProxy),
        cv.Required(CONF_PROXY_ON): cv.use_id(switch.Switch),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await smart_display.register_plugin(var, __file__)
    cg.add(var.set_proxy_on(await cg.get_variable(config[CONF_PROXY_ON])))
