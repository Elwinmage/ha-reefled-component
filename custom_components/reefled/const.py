from homeassistant.const import Platform

DOMAIN = "reefled"

DEVICE_MANUFACTURER="Red Sea"

CONF_FLOW_PLATFORM = "platform"

PLATFORMS: list[Platform] = [Platform.LIGHT]

CONFIG_FLOW_IP_ADDRESS="ip_address"

DEFAULT_PULL_RATE=120
