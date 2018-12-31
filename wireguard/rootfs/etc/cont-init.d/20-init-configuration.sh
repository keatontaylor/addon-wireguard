#!/usr/bin/with-contenv bash
# ==============================================================================
# Hass.io Add-ons: WireGuard
# Creates WireGuard configuration and private key in case it is non-existing
# ==============================================================================
# shellcheck disable=SC1091
source /usr/lib/hassio-addons/base.sh

declare -r DATA_PATH="/data"
declare -r CONFIG_PATH="/etc/wireguard"
declare -r CONFIG_FILE="${CONFIG_PATH}/wg0.conf"
declare -r CONFIG_PRIVATE_KEY="${CONFIG_PATH}/private_key"
declare -r PRIVATE_KEY_PATH="${DATA_PATH}/private_key"
declare PRIVATE_KEY

mkdir -p $CONFIG_PATH \
    || hass.die 'Failed to create WireGuard config directory'

echo "[Interface]" > $CONFIG_FILE \
    || hass.die 'Failed to create WireGuard interface config file'

# Add listen port to config
echo "ListenPort =" `hass.config.get 'port'` >> $CONFIG_FILE \
    || hass.die 'Failed to add listen port to config file'

# Check for user defined private key
PRIVATE_KEY=`hass.config.get 'private_key'`
if [[ -z $PRIVATE_KEY ]]; then
    # Check for previously generated private key
    if ! hass.file_exists $PRIVATE_KEY_PATH; then
        hass.log.info 'Generating private key'

        umask 077 \
        && wg genkey > $PRIVATE_KEY_PATH \
            || hass.die 'Failed to create private key for interface'
    else
        hass.log.info 'Using previously generated private key'
    fi
    cp $PRIVATE_KEY_PATH $CONFIG_PRIVATE_KEY \
        || hass.die 'Failed to copy stored private key to config directory'
    PRIVATE_KEY=`cat $PRIVATE_KEY_PATH`
else
    hass.log.info 'Using user defined private key'
    echo $PRIVATE_KEY > $CONFIG_PRIVATE_KEY \
        || hass.die 'Failed to store private key in config directory'
fi
hass.log.info 'Private key is' $PRIVATE_KEY
hass.log.info 'Public key is' `wg pubkey < $CONFIG_PRIVATE_KEY`

# Add private key to config
echo "PrivateKey =" $PRIVATE_KEY >> $CONFIG_FILE \
    || hass.die 'Failed to add private key to config file'

echo >> $CONFIG_FILE \
    || hass.die 'Failed to add newline to end of interface section'
