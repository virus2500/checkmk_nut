#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
'''
Module for the NUT agent-based check.

This module parses the output from the NUT UPS monitoring tool, discovers available UPS services,
and performs checks against defined thresholds.
'''
# (c) 2022-2023 Marcel Pennewiss <opensource@pennewiss.de>

# Contributions:
# Christian Kreidl (christian.kreidl@ziti.uni-heidelberg.de)
# Marco (github.com/Marco98)

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from typing import (
    Any,
    Callable,
    Dict,
    Mapping,
    TypedDict,
    Tuple,
)

from cmk.agent_based.v2 import (
    AgentSection,
    DiscoveryResult,
    check_levels,
    render,
    CheckPlugin,
    CheckResult,
    Result,
    Service,
    StringTable,
    State
)

# from plugins.nut.web.plugins.wato import nut

# pylint: disable=W0105
'''example output from nut
# <<<nut>>>
# ==> demo_ups <==
# demo_ups battery.charge: 100
# demo_ups battery.packs: 6
# demo_ups battery.runtime: 788
# demo_ups battery.voltage: 2.16
# demo_ups battery.voltage.high: 62.4
# demo_ups battery.voltage.low: 78
# demo_ups battery.voltage.nominal: 12
# demo_ups device.type: ups
# demo_ups driver.flag.novendor: enabled
# demo_ups driver.name: blazer_usb
# demo_ups driver.parameter.pollinterval: 2
# demo_ups driver.parameter.port: auto
# demo_ups driver.parameter.productid: 0005
# demo_ups driver.parameter.protocol: megatec
# demo_ups driver.parameter.runtimecal: 270,100,594,50
# demo_ups driver.parameter.subdriver: phoenix
# demo_ups driver.parameter.vendorid: 06da
# demo_ups driver.version: 2.7.2
# demo_ups driver.version.internal: 0.11
# demo_ups input.frequency: 50.0
# demo_ups input.voltage: 238.0
# demo_ups input.voltage.fault: 0.0
# demo_ups output.voltage: 229.9
# demo_ups ups.beeper.status: disabled
# demo_ups ups.delay.shutdown: 30
# demo_ups ups.delay.start: 180
# demo_ups ups.load: 39
# demo_ups ups.productid: 0005
# demo_ups ups.status: OL
# demo_ups ups.temperature: 27.8
# demo_ups ups.type: online
# demo_ups ups.vendorid: 06da
'''

Metrics = Dict[str, int]


class UpsData(TypedDict, total=False):
    '''TypedDict to define the model for UPS data.'''
    battery_charge: float
    battery_packs: int
    battery_runtime: float
    battery_voltage: float
    input_frequency: float
    input_voltage: float
    input_voltage_fault: float
    output_voltage: float
    ups_beeper_status: str
    ups_load: float
    ups_temperature: float


Section = Dict[str, UpsData]


def nut_parse(string_table: StringTable) -> Section:
    '''
    Parse the input string table from the NUT UPS output into a structured section.

    Args:
        string_table (StringTable): The raw string table lines from the agent output.

    Returns:
        Section: A dictionary mapping UPS names to their respective data.
    '''

    parsed: Section = {}

    for idx, line in enumerate(string_table):

        if line[0] == "==>" and line[-1] == "<==":
            # Found section beginning
            ups_name = " ".join(string_table[idx][1:-1])
            parsed[ups_name] = {}

        elif len(line) >= 2:
            # Found key value pair
            key = line[0]
            val = " ".join(line[1:])

            # Fix key
            key = key.replace('.', '_').replace(':', '')

            # Convert several keys/values
            if key in [
                    'battery_charge',
                    'battery_runtime',
                    'battery_voltage',
                    'input_frequency',
                    'input_voltage',
                    'input_voltage_fault',
                    'output_voltage',
                    'ups_load',
                    'ups_temperature'
            ]:
                parsed[ups_name][key] = float(val)
            elif key in ['battery_packs']:
                parsed[ups_name][key] = int(val)
            elif key in ['ups_status', 'ups_beeper_status']:
                parsed[ups_name][key] = val

    return parsed


def discover_nut(section: Section) -> DiscoveryResult:
    '''
    Discover UPS services based on the parsed section.

    Args:
        section (Section): The parsed UPS data.

    Yields:
        DiscoveryResult: A discovery result for each UPS service found.
    '''

    for ups_name, ups_data in section.items():
        if len(ups_data) > 0:
            yield Service(item=ups_name)


_METRIC_SPECS: Mapping[str, Tuple[str, Callable, bool, bool, bool]] = {
    # 'metric': ('Metric Name', renderer, notice_only, lower_levels, upper_levels)
    'battery_charge': ('Battery charge', render.percent, False, True, False),
    'battery_runtime': ('Battery runtime', render.timespan, False, True, False),
    'battery_voltage': ('Battery voltage', lambda v: f"{v:0.2f} V", True, True, False),
    'input_frequency': ('Input frequency', render.frequency, True, True, True),
    'input_voltage': ('Input voltage', lambda v: f"{v:0.2f} V", True, True, True),
    'input_voltage_fault': ('Input voltage (fault)', lambda v: f"{v:0.2f} V", True, False, True),
    'output_voltage': ('Output voltage', lambda v: f"{v:.2f} V", True, True, True),
    'ups_load': ('Load', render.percent, False, True, True),
    'ups_temperature': ('Temperature', lambda v: f"{v:0.1f} °C", True, False, True),
}


_STATUS_SPECS: Mapping[str, Tuple[State, str]] = {
    # 'Status': (State, 'State summary') based on
    # https://github.com/networkupstools/nut/blob/master/docs/new-drivers.txt ("Status data")
    'OL': (State.OK, 'On line'),
    'OB': (State.WARN, 'On battery'),
    'LB': (State.CRIT, 'Low battery'),
    'HB': (State.WARN, 'High battery'),
    'RB': (State.WARN, 'Replace battery'),
    'CHRG': (State.OK, 'Charging'),
    'DISCHRG': (State.WARN, 'Discharging'),
    'BYPASS': (State.WARN, 'Bypass'),
    'CAL': (State.WARN, 'Calibrating'),
    'OFF': (State.CRIT, 'Switched off'),
    'OVER': (State.CRIT, 'Overloaded'),
    'TRIM': (State.WARN, 'Trimming incoming voltage'),
    'BOOST': (State.WARN, 'Boosting incoming voltage'),
}


def check_nut(item: str, params: Mapping[str, Any], section: Section) -> CheckResult:
    '''
    Check the UPS data for the specified item against provided parameters.

    Args:
        item (str): The UPS item name.
        params (Mapping[str, Any]): The check parameters including thresholds and settings.
        section (Section): The parsed UPS data section.

    Yields:
        CheckResult: A series of results based on UPS status and metric checks.
    '''
    # print(params)
    ups_data = section.get(item)

    # Check if the UPS data is available
    if ups_data is None:
        yield Result(
            state=State.UNKNOWN,
            summary="Could not find data in output"
        )
        return

    # Check UPS status
    # print(f"Checking UPS: {item}")
    for status in ups_data['ups_status'].split():
        # print(f"Status: {status}")
        if status in _STATUS_SPECS:
            yield Result(
                state=_STATUS_SPECS[status][0],
                summary=f"Status: {_STATUS_SPECS[status][1]} ({status})"
            )
        else:
            yield Result(
                state=State.UNKNOWN,
                summary=f"Unknown status: {status}"
            )

    # Check Beeper status
    current_beeper_status = ups_data.get('ups_beeper_status')
    # Check expected Beeper status set by user
    expected_beeper_status = params.get('ups_beeper_status')

    if expected_beeper_status not in ("ignore", current_beeper_status):
        yield Result(
            state=State.CRIT,
            summary=f"Beeper: {ups_data.get('ups_beeper_status', 'disabled')}"
        )

    # Check all metrics
    for metric in ups_data:
        # print(f"Metric: {metric}, Value: {ups_data[metric]}")
        # Ignore unspecified metrics
        if metric not in _METRIC_SPECS:
            continue

        # Calculate real voltage
        if metric == 'battery_voltage':
            ups_data[metric] = ups_data[metric] * ups_data.get('battery_packs', 1)

        metric_params = params.get(metric)

        if isinstance(metric_params, dict):
            levels_lower = metric_params.get("lower", None)
            levels_upper = metric_params.get("upper", None)
        else:
            # If metric_params is a simple value (like a fixed threshold),
            levels_lower = metric_params if metric_params is not None else None
            levels_upper = None

        yield from check_levels(
            ups_data[metric],
            metric_name=f"nut_{metric}",
            label=_METRIC_SPECS[metric][0],
            levels_lower=levels_lower,
            levels_upper=levels_upper,
            render_func=_METRIC_SPECS[metric][1],
            notice_only=_METRIC_SPECS[metric][2],
            boundaries=(0, None),
        )


agent_section_nut = AgentSection(
    name="nut",
    parse_function=nut_parse,
)


check_plugin_nut = CheckPlugin(
    name="nut",
    service_name="UPS %s",
    discovery_function=discover_nut,
    check_function=check_nut,
    sections=["nut"],
    check_default_parameters={
        'battery_charge': ("fixed", (90, 85)),
        'battery_runtime': ("fixed", (1200, 900)),
        'battery_voltage': ("fixed", (10, 5)),
        'input_frequency': {
            'lower': ('fixed', (49, 45)),
            'upper': ('fixed', (51, 55))
        },
        'input_voltage': {
            'lower': ('fixed', (0, 0)),
            'upper': ('fixed', (245, 250))
        },
        'output_voltage': {
            'lower': ('fixed', (0, 0)),
            'upper': ('fixed', (245, 250))
        },
        'input_voltage_fault': ("fixed", (155, 160)),
        'ups_beeper_status': 'enabled',
        'ups_load': {
            'lower': ('fixed', (0, 0)),
            'upper': ('fixed', (50, 70))
        },
        'ups_temperature': ("fixed", (35, 40)),
    },
    check_ruleset_name="nut",
)
