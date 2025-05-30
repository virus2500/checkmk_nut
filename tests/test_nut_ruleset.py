#!/usr/bin/env python3
'''Ruleset tests for the NUT plugin in Checkmk.'''
from collections.abc import Mapping
from cmk.rulesets.v1.form_specs import SimpleLevels, DictElement
from cmk.rulesets.v1.rule_specs import CheckParameters
from plugins.nut.rulesets.nut import _migrate, _parameter_valuespec_nut, rule_spec_nut


def test_migrate_single_levels():
    # Tuple of length 2 without fixed tag should convert to fixed
    original = (10, 5)
    migrated = _migrate(original)
    assert isinstance(migrated, tuple)
    assert migrated[0] == "fixed"
    assert migrated[1] == (10, 5)

    # Tuple of length 4 should become dict with lower/upper
    original4 = (49, 45, 51, 55)
    migrated4 = _migrate(original4)
    assert isinstance(migrated4, dict)
    assert migrated4["lower"] == ("fixed", (49, 45))
    assert migrated4["upper"] == ("fixed", (51, 55))


def test_migrate_nested_dict():
    nested = {"input_frequency": (49, 45, 51, 55), "battery_charge": (90, 85)}
    result = _migrate(nested)
    assert isinstance(result, Mapping)
    # input_frequency should be dict with lower/upper
    assert isinstance(result["input_frequency"], dict)
    assert result["input_frequency"]["lower"] == ("fixed", (49, 45))
    assert result["input_frequency"]["upper"] == ("fixed", (51, 55))
    # battery_charge should be tuple fixed
    assert result["battery_charge"] == ("fixed", (90, 85))


def test_parameter_valuespec_structure():
    spec = _parameter_valuespec_nut()
    assert hasattr(spec, "elements")
    # Check battery_charge element exists and is DictElement wrapping SimpleLevels
    bc_elem = spec.elements.get("battery_charge")
    assert isinstance(bc_elem, DictElement)
    sl = bc_elem.parameter_form
    assert isinstance(sl, SimpleLevels)
    assert sl.level_direction.name == "LOWER"
    # Check input_frequency nested dict
    ifreq_elem = spec.elements.get("input_frequency")
    nested = ifreq_elem.parameter_form
    assert hasattr(nested, "elements")
    assert "lower" in nested.elements and "upper" in nested.elements


def test_rule_spec_nut():
    spec = rule_spec_nut
    # Must be instance of CheckParameters
    assert isinstance(spec, CheckParameters)
    assert spec.name == "nut"
    assert spec.topic.name.lower() == "applications"
    # Check that calling parameter_form returns a structure
    param_form = spec.parameter_form()
    assert hasattr(param_form, "elements")
    # Ensure ups_beeper_status has choices
    ub = param_form.elements.get("ups_beeper_status")
    choices = {e.name for e in ub.parameter_form.elements}
    assert choices == {"enabled", "disabled", "ignore"}
