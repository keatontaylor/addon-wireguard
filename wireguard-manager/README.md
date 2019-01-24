# Hass.io Add-ons: WireGuard Manager

![WireGuard screenshot][screenshot]

WireGuard VPN for Home Assistant

## About

WireGuard® is an extremely simple yet fast and modern VPN that utilizes 
state-of-the-art cryptography. It aims to be faster, simpler, leaner, and 
more useful than IPSec, while avoiding the massive headache. It intends to 
be considerably more performant than OpenVPN. WireGuard is designed as a 
general purpose VPN for running on embedded interfaces and super computers 
alike, fit for many different circumstances.

## Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Hass.io add-on.

1. [Add our Hass.io add-ons repository][repository] to your Hass.io instance.
1. Install the "WireGuard" add-on.
1. Start the "WireGuard" add-on
1. Check the logs of the "WireGuard" add-on to see if everything went well.

## Configuration

**Note**: _Remember to restart the add-on when the configuration is changed._

Example add-on configuration:

```json
{
  "log_level": "info",
  "port": 51820
}
```

**Note**: _This is just an example, don't copy and past it! Create your own!_

### Option: `log_level`

The `log_level` option controls the level of log output by the addon and can
be changed to be more or less verbose, which might be useful when you are
dealing with an unknown issue. Possible values are:

- `trace`: Show every detail, like all called internal functions.
- `debug`: Shows detailed debug information.
- `info`: Normal (usually) interesting events.
- `warning`: Exceptional occurrences that are not errors.
- `error`:  Runtime errors that do not require immediate action.
- `fatal`: Something went terribly wrong. Add-on becomes unusable.

Please note that each level automatically includes log messages from a
more severe level, e.g., `debug` also shows `info` messages. By default,
the `log_level` is set to `info`, which is the recommended setting unless
you are troubleshooting.

These log level also affects the log levels of the AppDaemon.

### Option: `port`

Allows you to specify the TCP port used for the WireGuard Manager.

**Note**: _WireGuard interface ports will be configured from user interface._


## WireGuard configuration

For more information about configuring WireGuard, please refer to the
extensive documentation they offer:

<https://www.wireguard.com/>

[repository]: https://github.com/whiskerz007/addon-wireguard
[screenshot]: https://github.com/whiskerz007/addon-wireguard/raw/master/images/screenshot.png
