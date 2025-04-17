from homeassistant.const import Platform

DOMAIN = "reefled"

DEVICE_MANUFACTURER="Red Sea"

CONF_FLOW_PLATFORM = "platform"

PLATFORMS: list[Platform] = [Platform.LIGHT,Platform.SENSOR]

CONFIG_FLOW_IP_ADDRESS="ip_address"

SCAN_INTERVAL=120

FAN_INTERNAL_NAME='fan'
TEMPERATURE_INTERNAL_NAME="temperature"
WHITE_INTERNAL_NAME="white"
BLUE_INTERNAL_NAME="blue"
MOON_INTERNAL_NAME="moon"

CONVERSION_COEF=100/255

