#!/usr/bin/env python3
'''Agent tests for the NUT plugin in Checkmk.'''

from cmk.agent_based.v2 import Result, State
from plugins.nut.agent_based.nut import nut_parse, check_nut


def test_nut_parse_basic():
    string_table = [
        ["==>", "demo_ups", "<=="],
        ["battery.charge:", "100"],
        ["battery.runtime:", "788"],
        ["battery.packs:", "2"],
        ["ups.status:", "OL"],
    ]
    parsed = nut_parse(string_table)
    assert "demo_ups" in parsed
    assert parsed["demo_ups"]["battery_charge"] == 100.0
    assert parsed["demo_ups"]["battery_runtime"] == 788.0
    assert parsed["demo_ups"]["battery_packs"] == 2
    assert parsed["demo_ups"]["ups_status"] == "OL"


def test_check_nut_status_ok():
    section = {
        "demo_ups": {
            "ups_status": "OL",
            "ups_beeper_status": "enabled",
            "battery_charge": 100.0,
            "battery_packs": 1,
        }
    }
    params = {
        "ups_beeper_status": "enabled",
        "battery_charge": ("fixed", (90, 85)),
    }
    results = list(check_nut("demo_ups", params, section))
    states = [r.state for r in results if isinstance(r, Result)]
    assert State.OK in states


def test_check_nut_status_low_battery():
    section = {
        "demo_ups": {
            "ups_status": "LB",
            "ups_beeper_status": "disabled",
            "battery_charge": 20.0,
            "battery_packs": 1,
        }
    }
    params = {
        "ups_beeper_status": "enabled",
        "battery_charge": ("fixed", (90, 85)),
    }
    results = list(check_nut("demo_ups", params, section))
    states = [r.state for r in results if isinstance(r, Result)]
    assert State.CRIT in states


def test_check_nut_unknown_status():
    section = {
        "demo_ups": {
            "ups_status": "INVALID",
            "ups_beeper_status": "enabled",
            "battery_charge": 100.0,
        }
    }
    params = {
        "ups_beeper_status": "enabled",
        "battery_charge": ("fixed", (90, 85)),
    }
    results = list(check_nut("demo_ups", params, section))
    states = [r.state for r in results if isinstance(r, Result)]
    summaries = [r.summary for r in results if isinstance(r, Result)]
    assert State.UNKNOWN in states
    assert any("Unknown status: INVALID" in s for s in summaries)


def test_check_nut_beeper_status_critical():
    section = {
        "demo_ups": {
            "ups_status": "OL",
            "ups_beeper_status": "disabled",
            "battery_charge": 100.0,
        }
    }
    params = {
        "ups_beeper_status": "enabled",
    }
    results = list(check_nut("demo_ups", params, section))
    states = [r.state for r in results if isinstance(r, Result)]
    summaries = [r.summary for r in results if isinstance(r, Result)]
    assert State.CRIT in states
    assert any("Beeper: disabled" in s for s in summaries)
