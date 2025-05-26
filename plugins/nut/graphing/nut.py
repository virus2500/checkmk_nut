#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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

# from cmk.gui.plugins.metrics import metric_info
from cmk.graphing.v1 import Title
# from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, Unit, TimeNotation
from cmk.graphing.v1.perfometers import Closed, FocusRange, Perfometer

metric_nut_battery_charge = Metric(
    name="nut_battery_charge",
    title=Title("Battery charge"),
    unit=Unit(DecimalNotation("%")),
    color=Color.LIGHT_BLUE,
)

metric_nut_battery_runtime = Metric(
    name="nut_battery_runtime",
    title=Title("Battery runtime"),
    unit=Unit(TimeNotation()),
    color=Color.BLUE,
)

metric_nut_battery_voltage = Metric(
    name="nut_battery_voltage",
    title=Title("Battery voltage"),
    unit=Unit(DecimalNotation("V")),
    color=Color.GREEN,
)

metric_nut_input_frequency = Metric(
    name="nut_input_frequency",
    title=Title("Input frequency"),
    unit=Unit(DecimalNotation("1/s")),
    color=Color.YELLOW,
)

metric_nut_input_voltage = Metric(
    name="nut_input_voltage",
    title=Title("Input voltage"),
    unit=Unit(DecimalNotation("V")),
    color=Color.YELLOW,
)

metric_nut_input_voltage_fault = Metric(
    name="nut_input_voltage_fault",
    title=Title("Input voltage (fault)"),
    unit=Unit(DecimalNotation("V")),
    color=Color.RED,
)

metric_nut_output_voltage = Metric(
    name="nut_output_voltage",
    title=Title("Output voltage"),
    unit=Unit(DecimalNotation("V")),
    color=Color.GREEN,
)

metric_nut_ups_load = Metric(
    name="nut_ups_load",
    title=Title("Load"),
    unit=Unit(DecimalNotation("%")),
    color=Color.GREEN,
)

metric_nut_ups_temperature = Metric(
    name="nut_ups_temperature",
    title=Title("Temperature"),
    unit=Unit(DecimalNotation("C")),
    color=Color.BROWN,
)

perfometer_nut = Perfometer(
    name="nut",
    focus_range=FocusRange(Closed(0), Closed(100)),
    segments=["nut_battery_charge"],
)
