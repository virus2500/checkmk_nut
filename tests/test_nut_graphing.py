#!/usr/bin/env python3
'''Graphing tests for the NUT plugin in Checkmk.'''
from cmk.graphing.v1.metrics import Color, DecimalNotation
from cmk.graphing.v1.perfometers import FocusRange
from cmk.graphing.v1 import Title
from plugins.nut.graphing import nut


def test_all_metric_names():
    metrics = [
        nut.metric_nut_battery_charge,
        nut.metric_nut_battery_runtime,
        nut.metric_nut_battery_voltage,
        nut.metric_nut_input_frequency,
        nut.metric_nut_input_voltage,
        nut.metric_nut_input_voltage_fault,
        nut.metric_nut_output_voltage,
        nut.metric_nut_ups_load,
        nut.metric_nut_ups_temperature,
    ]
    metric_names = {m.name for m in metrics}
    expected_names = {
        "nut_battery_charge",
        "nut_battery_runtime",
        "nut_battery_voltage",
        "nut_input_frequency",
        "nut_input_voltage",
        "nut_input_voltage_fault",
        "nut_output_voltage",
        "nut_ups_load",
        "nut_ups_temperature",
    }
    assert metric_names == expected_names


def test_metric_attributes():
    m = nut.metric_nut_battery_charge
    assert m.title == Title("Battery charge")
    assert isinstance(m.unit.notation, DecimalNotation)
    assert m.unit.notation.symbol == "%"
    assert m.color == Color.LIGHT_BLUE


def test_perfometer_nut_definition():
    p = nut.perfometer_nut
    assert p.name == "nut"
    assert list(p.segments) == ["nut_battery_charge"]
    fr = p.focus_range
    assert isinstance(fr, FocusRange)
    assert fr.lower.value == 0
    assert fr.upper.value == 100
