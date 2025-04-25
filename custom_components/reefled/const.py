from homeassistant.const import Platform

DOMAIN = "reefled"

DEVICE_MANUFACTURER="Red Sea"

CONF_FLOW_PLATFORM = "platform"

PLATFORMS: list[Platform] = [Platform.LIGHT,Platform.SENSOR,Platform.BINARY_SENSOR,Platform.SWITCH]

CONFIG_FLOW_IP_ADDRESS="ip_address"

SCAN_INTERVAL=120

FAN_INTERNAL_NAME='fan'
TEMPERATURE_INTERNAL_NAME="temperature"
WHITE_INTERNAL_NAME="white"
BLUE_INTERNAL_NAME="blue"
MOON_INTERNAL_NAME="moon"
STATUS_INTERNAL_NAME="status"
IP_INTERNAL_NAME="ip"


MODEL_NAME="hw_model"
MODEL_ID="hwid"
HW_VERSION="hw_revision"
SW_VERSION="version"


DAILY_PROG_INTERNAL_NAME="daily_prog"

VIRTUAL_LED="virtual"

CONVERSION_COEF=100/255

DAYS=["Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
