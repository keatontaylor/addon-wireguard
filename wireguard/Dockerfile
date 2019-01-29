ARG BUILD_FROM=hassioaddons/base:2.3.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

ENV WG_I_PREFER_BUGGY_USERSPACE_TO_POLISHED_KMOD=1

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup base
RUN \
    apk add --no-cache --virtual .build-dependencies \
        build-base=0.5-r1 \
        git=2.18.1-r0 \
    \
    && apk add --no-cache \
        go@edge=1.11.5-r0 \
        iptables=1.6.2-r0 \
        wireguard-tools-wg@edge=0.0.20190123-r2 \
    \
    && git clone --branch "0.0.20181222" --depth=1 \
        "https://git.zx2c4.com/wireguard-go" /tmp/wireguard \
    \
    && cd /tmp/wireguard \
    && make \
    && make install \
    \
    && rm -rf /tmp/* \
    && apk del --purge --force-broken-world .build-dependencies \
    && apk del --purge --force-broken-world go

# Copy root filesystem
COPY rootfs /

# Build arugments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="WireGuard" \
    io.hass.description="WireGuard VPN" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="whiskerz007 <2713522+whiskerz007@users.noreply.github.com>" \
    org.label-schema.description="WireGuard VPN for Home Assistant" \
    org.label-schema.build-date=${BUILD_DATE} \
    org.label-schema.name="WireGuard" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.url="https://github.com/whiskerz007/addon-wireguard" \
    org.label-schema.usage="https://github.com/whiskerz007/addon-wireguard/blob/master/wireguard/README.md" \
    org.label-schema.vcs-ref=${BUILD_REF} \
    org.label-schema.vcs-url="https://github.com/whiskerz007/addon-wireguard" \
    org.label-schema.vendor="whiskerz007"
