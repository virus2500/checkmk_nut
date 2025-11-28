# Checkmk Extension: Network UPS Tools (NUT) Monitoring

This project is a Checkmk extension designed to monitor UPS (Uninterruptible Power Supply) data using [Network UPS Tools (NUT)](https://networkupstools.org/).

It provides comprehensive monitoring capabilities, including metrics for battery charge, runtime, voltage, input/output frequencies, and more.

Additionally, it includes an agent bakery implementation to automate the deployment of the `nut.sh` plugin for Checkmk agents.

## Features

- **UPS Monitoring**:
  - Monitors key UPS metrics such as battery charge, runtime, voltage, input/output frequencies, load, and temperature.
  - Supports customizable thresholds for warnings and critical states.
  - Provides detailed status checks for UPS states (e.g., "On battery," "Low battery," "Overloaded").

- **Agent Bakery Integration**:
  - Automates the deployment of the `nut.sh` plugin to hosts via the Checkmk agent bakery.
  - Configurable deployment rules for enabling or disabling the plugin on specific hosts.

- **Graphing and Visualization**:
  - Includes predefined metrics for graphing UPS data in Checkmk.
  - Visualizes metrics such as battery charge, runtime, voltage, and load with color-coded graphs.

## Installation

### Manual Installation Guide (Client & Server)
This section describes how to manually install the NUT plugin on both the Checkmk server and the monitored client, which is running NUT-Server.  

> ⚠️ **Important:** Tested with **Checkmk Raw Edition 2.4.0p14** and a local **NUT server** (`upsd`) running on the monitored host.

**Server Installation**

Install the Checkmk extension package (`mkp`) on the server:
```bash
# Switch to your Checkmk site user (e.g., cmk)
su - cmk

# Download the NUT plugin package (mkp) to /tmp
wget https://github.com/virus2500/checkmk_nut/releases/download/<version>/nut-<version>.mkp -O /tmp/

# Add the mkp package to the Checkmk installation
mkp add /tmp/nut-<version>.mkp

# Enable the NUT plugin in Checkmk
mkp enable nut

# List all installed mkp packages to verify installation
mkp list 
```

**Client Installation**

```bash
# Download the plugin script to the Checkmk agent plugins directory
# Option 1: From the internet
wget https://raw.githubusercontent.com/virus2500/checkmk_nut/refs/heads/main/local/share/check_mk/agents/plugins/nut.sh -O /usr/lib/check_mk_agent/plugins/nut.sh

# Option 2: If your agent host has no internet access, copy it from the Checkmk site
scp ~/local/share/check_mk/agents/plugins/nut.sh user@target-host:/tmp/
sudo mv /tmp/nut.sh /usr/lib/check_mk_agent/plugins/nut.sh

# Make the script executable
chmod +x /usr/lib/check_mk_agent/plugins/nut.sh 
```

See [MPK install](https://docs.checkmk.com/latest/en/mkps.html) for more information


## Contributing
Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the GNU General Public License v2. See the LICENSE file for details.

## Acknowledgments
Inspired by the original NUT plugin by Daniel Karni and [Marcel Pennewiss](https://github.com/mape2k/).

## References
[Network UPS Tools (NUT)](https://networkupstools.org/)

[Checkmk](https://checkmk.com/)
