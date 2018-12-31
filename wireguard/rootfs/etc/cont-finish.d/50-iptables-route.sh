#!/usr/bin/with-contenv bash
# ==============================================================================
# Hass.io Add-ons: WireGuard
# Remove routes to iptables for each address on WireGuard interface on shutdown
# ==============================================================================
# shellcheck disable=SC1091
source /usr/lib/hassio-addons/base.sh

# Cleanup iptable rules if gateway is true
if hass.config.true 'gateway'; then
    # Remove jump rule from POSTROUTING chain
    if `iptables -t nat -C POSTROUTING -j WIREGUARD`; then
        iptables -t nat -D POSTROUTING -j WIREGUARD \
            || hass.die 'Failed to remove jump rule from POSTROUTING chain'
    fi

    # Flush WIREGUARD chain
    iptables -t nat -F WIREGUARD \
        || hass.die "Failed to flush WIREGUARD chain"

    # Remove WIREGUARD chain
    iptables -t nat -X WIREGUARD \
        || hass.die 'Failed to remove WIREGUARD chain'
fi
