#!/usr/bin/with-contenv bash
# ==============================================================================
# Hass.io Add-ons: WireGuard
# Add to WireGuard configuration for each peer
# ==============================================================================
# shellcheck disable=SC1091
source /usr/lib/hassio-addons/base.sh

declare -r CONFIG_PATH="/etc/wireguard"
declare -r CONFIG_FILE="${CONFIG_PATH}/wg0.conf"

# Process all peers
for peer in `echo $(hass.config.get 'peers') | jq -c '.'`; do
    echo "[Peer]" >> $CONFIG_FILE \
        || hass.die 'Failed to add peer section to config file'

    # Add peer public key
    if [[ `echo $peer | jq -r '.public_key'` ]]; then
        echo "PublicKey =" `echo $peer | jq -r '.public_key'` >> $CONFIG_FILE \
            || hass.die 'Failed to add peer public key config file'
    fi

    # Add peer preshared key
    if [[ `echo $peer | jq -r '.preshared_key'` ]]; then
        echo "PresharedKey =" `echo $peer | jq -r '.preshared_key'` >> $CONFIG_FILE \
            || hass.die 'Failed to add peer preshared key config file'
    fi

    # Add peer endpoint
    if [[ `echo $peer | jq -r '.endpoint'` ]]; then
        echo "Endpoint =" `echo $peer | jq -r '.endpoint'` >> $CONFIG_FILE \
            || hass.die 'Failed to add peer endpoint config file'
    fi

    # Add peer allowed ips
    if [[ `echo $peer | jq -r '.allowed_ips'` ]]; then
        for ip in $(echo $peer | jq -c '.allowed_ips'); do
            echo "AllowedIPs =" `echo $ip | jq -r '.[]' | tr '\n' ', ' | sed 's/.$//'` >> $CONFIG_FILE \
                || hass.die 'Failed to add peer allowed ips config file'
        done
    fi

    # Add peer keepalive
    if [[ `echo $peer | jq -r '.keepalive'` ]]; then
        echo "PersistentKeepalive =" `echo $peer | jq -r '.keepalive'` >> $CONFIG_FILE \
            || hass.die 'Failed to add peer keepalive config file'
    fi

    echo >> $CONFIG_FILE \
        || hass.die 'Failed to add newline to end of peer section'
done
