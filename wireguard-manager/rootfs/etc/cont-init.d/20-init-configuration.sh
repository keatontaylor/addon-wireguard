#!/usr/bin/with-contenv bash
# ==============================================================================
# Hass.io Add-ons: WireGuard
# Creates WireGuard configuration directory and checks if port is in use
# ==============================================================================
# shellcheck disable=SC1091
source /usr/lib/hassio-addons/base.sh

declare -r CONFIG_PATH="/etc/wireguard"
declare -r PORTS_IN_USE=($(netstat -lntu | sed -rne '/^tcp/ s/.*:([0-9]+)\>.*/\1/p}'))

mkdir -p $CONFIG_PATH \
    || hass.die 'Failed to create WireGuard config directory'

for port in ${PORTS_IN_USE[@]}; do
    if [ `hass.config.get 'port'` -eq $port ]; then
        hass.die 'Failed to use configured port, already in use'
    fi
done