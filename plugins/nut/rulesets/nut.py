#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Description:
    This module defines the rule specifications for monitoring UPS (Uninterruptible Power Supply) parameters
    using Network UPS Tools (NUT).
'''
from cmk.rulesets.v1.form_specs import (
    DictElement,
    LevelDirection,
    SimpleLevels,
    DefaultValue,
    Integer,
    Float,
    SingleChoiceElement,
    SingleChoice,
)

from cmk.rulesets.v1.rule_specs import (
    Dictionary,
    CheckParameters,
    Topic,
    HostCondition,
    Help,
)

from cmk.rulesets.v1 import Title


def _parameter_valuespec_nut():
    return Dictionary(
        elements={
            "battery_charge": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Battery charge"),
                    help_text=Help("Set the levels for the minimum charge amount of the battery."),
                    form_spec_template=Integer(unit_symbol="%"),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue(value=(90, 85)),
                )
            ),
            "battery_runtime": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Battery runtime"),
                    help_text=Help("Set the levels for the minimum runtime of the battery."),
                    form_spec_template=Integer(unit_symbol="sec"),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue(value=(1200, 900)),
                )
            ),
            "battery_voltage": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Battery voltage"),
                    help_text=Help("Set the levels for the minimum voltage of the battery."),
                    form_spec_template=Integer(unit_symbol="V"),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue(value=(12, 11)),
                )
            ),
            "input_frequency": DictElement(
                parameter_form=Dictionary(
                    title=Title("Input frequency"),
                    elements={
                        "lower": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Input frequency (lower threshold)"),
                                help_text=Help("Set the warning and critical levels for the minimum input frequency."),
                                form_spec_template=Integer(unit_symbol="Hz"),
                                level_direction=LevelDirection.LOWER,
                                prefill_fixed_levels=DefaultValue(value=(49, 45)),
                            )
                        ),
                        "upper": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Input frequency (upper threshold)"),
                                help_text=Help("Set the warning and critical levels for the maximum input frequency."),
                                form_spec_template=Integer(unit_symbol="Hz"),
                                level_direction=LevelDirection.UPPER,
                                prefill_fixed_levels=DefaultValue(value=(51, 55)),
                            )
                        ),
                    }
                )
            ),
            "input_voltage": DictElement(
                parameter_form=Dictionary(
                    title=Title("Input voltage"),
                    elements={
                        "lower": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Input voltage (lower threshold)"),
                                help_text=Help("Set the warning and critical levels for the minimum input voltage."),
                                form_spec_template=Integer(unit_symbol="V"),
                                level_direction=LevelDirection.LOWER,
                                prefill_fixed_levels=DefaultValue(value=(0, 0)),
                            )
                        ),
                        "upper": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Input voltage (upper threshold)"),
                                help_text=Help("Set the warning and critical levels for the maximum input voltage."),
                                form_spec_template=Integer(unit_symbol="V"),
                                level_direction=LevelDirection.UPPER,
                                prefill_fixed_levels=DefaultValue(value=(245, 250)),
                            )
                        ),
                    }
                )
            ),
            "output_voltage": DictElement(
                parameter_form=Dictionary(
                    title=Title("Output voltage"),
                    elements={
                        "lower": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Output voltage (lower threshold)"),
                                help_text=Help("Set the warning and critical levels for the minimum output voltage."),
                                form_spec_template=Integer(unit_symbol="V"),
                                level_direction=LevelDirection.LOWER,
                                prefill_fixed_levels=DefaultValue(value=(0, 0)),
                            )
                        ),
                        "upper": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Output voltage (upper threshold)"),
                                help_text=Help("Set the warning and critical levels for the maximum output voltage."),
                                form_spec_template=Integer(unit_symbol="V"),
                                level_direction=LevelDirection.UPPER,
                                prefill_fixed_levels=DefaultValue(value=(245, 250)),
                            )
                        ),
                    }
                )
            ),
            "input_voltage_fault": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Input voltage fault"),
                    help_text=Help("Set the levels for the minimum voltage of the input."),
                    form_spec_template=Integer(unit_symbol="V"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(155, 160)),
                )
            ),
            "ups_beeper_status": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Beeper status (normal state)"),
                    help_text=Help("Expected or acceptable state of the UPS beeper."),
                    elements=[
                        SingleChoiceElement(name="enabled", title=Title("Enabled")),
                        SingleChoiceElement(name="disabled", title=Title("Disabled")),
                        SingleChoiceElement(name="ignore", title=Title("Ignore")),
                    ],
                    prefill=DefaultValue("enabled"),
                )
            ),
            "ups_load": DictElement(
                parameter_form=Dictionary(
                    title=Title("UPS load"),
                    elements={
                        "lower": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Lower load threshold"),
                                help_text=Help("Warning/Critical when UPS load is too low."),
                                form_spec_template=Float(unit_symbol="%"),
                                level_direction=LevelDirection.LOWER,
                                prefill_fixed_levels=DefaultValue(value=(0.0, 0.0)),
                            )
                        ),
                        "upper": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Upper load threshold"),
                                help_text=Help("Warning/Critical when UPS load is too high."),
                                form_spec_template=Float(unit_symbol="%"),
                                level_direction=LevelDirection.UPPER,
                                prefill_fixed_levels=DefaultValue(value=(50.0, 70.0)),
                            )
                        ),
                    }
                )
            ),
            "ups_temperature": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Temperature (upper threshold)"),
                    help_text=Help("Set the levels for the temperature of the UPS."),
                    form_spec_template=Integer(unit_symbol="°C"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(35, 40)),
                )
            ),
        }
    )


rule_spec_nut = CheckParameters(
    name="nut",
    title=Title("Network UPS Tools"),
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_valuespec_nut,
)
