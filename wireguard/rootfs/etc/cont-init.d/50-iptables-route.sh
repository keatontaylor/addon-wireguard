#!/usr/bin/with-contenv bash
# ==============================================================================
# Hass.io Add-ons: WireGuard
# Add routes to iptables for each address on WireGuard interface
# ==============================================================================
# shellcheck disable=SC1091
source /usr/lib/hassio-addons/base.sh

# Add iptable rules if gateway is true
if hass.config.true 'gateway'; then
    # Add iptables chain
    iptables -t nat -N WIREGUARD \
        || hass.log.debug 'Chain already existed'

    # Add jump rule to POSTROUTING chain
    iptables -t nat -A POSTROUTING -j WIREGUARD \
        || hass.die 'Failed to add jump rule to POSTROUTING chain'

    # Add route for WireGuard IP address to access local networks
    iptables -t nat -A WIREGUARD -s `hass.config.get 'ip_address'` -j MASQUERADE \
        || hass.die 'Failed to add route for interface address to iptables'
fi
