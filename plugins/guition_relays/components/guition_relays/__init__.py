"""Guition relays: the relays of plugin.yaml (and the part `three`) on the screen's own settings page.

The relays themselves are ESPHome gpio switches; this component only knows them, so the settings page can switch them
on the glass. register_plugin() takes the id, version and the screen's texts from the manifest and translations/.
"""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import smart_display, switch
from esphome.const import CONF_ID

DEPENDENCIES = ["smart_display", "switch"]

RELAYS = ("relay_1", "relay_2", "relay_3")

guition_relays_ns = cg.esphome_ns.namespace("guition_relays")
GuitionRelays = guition_relays_ns.class_("GuitionRelays", cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(GuitionRelays),
        cv.Required(RELAYS[0]): cv.use_id(switch.Switch),
        **{cv.Optional(key): cv.use_id(switch.Switch) for key in RELAYS[1:]},
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await smart_display.register_plugin(var, __file__)
    for index, key in enumerate(RELAYS):
        if key in config:
            cg.add(var.set_relay(index, await cg.get_variable(config[key])))
