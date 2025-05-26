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

Download the latest mkp (zipped) from the releases page.
Install the unzipped mkp either via the GUI or via the CLI.

See [MPK install](https://docs.checkmk.com/latest/en/mkps.html) for more information

## Contributing
Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the GNU General Public License v2. See the LICENSE file for details.

## Acknowledgments
Inspired by the original NUT plugin by Daniel Karni and Marcel Pennewiss.

## References
[Network UPS Tools (NUT)](https://networkupstools.org/)

[Checkmk](https://checkmk.com/)