from homeassistant.const import Platform

DOMAIN = "reefled"

DEVICE_MANUFACTURER="Red Sea"

CONF_FLOW_PLATFORM = "platform"

PLATFORMS: list[Platform] = [Platform.LIGHT,Platform.SENSOR]

CONFIG_FLOW_IP_ADDRESS="ip_address"

DEFAULT_PULL_RATE=60

FAN_INTERNAL_NAME='Fan'
TEMPERATURE_INTERNAL_NAME="Temperature"
WHITE_INTERNAL_NAME="white"
BLUE_INTERNAL_NAME="blue"
MOON_INTERNAL_NAME="moon"
