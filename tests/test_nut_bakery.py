#!/usr/bin/env python3
'''Bakery tests for the NUT plugin in Checkmk.'''

from cmk.rulesets.v1 import Title
from plugins.nut.rulesets.cee.bakery_nut import rule_spec_bakery_nut


def test_bakery_rule_name_and_title():
    assert rule_spec_bakery_nut.name == "nut"
    assert rule_spec_bakery_nut.title == Title("Network UPS Tools agent plugin")


def test_bakery_rule_structure():
    param_form = rule_spec_bakery_nut.parameter_form()
    assert isinstance(param_form.elements, dict)
    assert "deploy" in param_form.elements

    deploy_elem = param_form.elements["deploy"]
    assert deploy_elem.required is True
    choice_form = deploy_elem.parameter_form

    assert choice_form.prefill.value == "yes"

    values = {e.name for e in choice_form.elements}
    assert "yes" in values
    assert "no" in values
