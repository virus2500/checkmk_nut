# #!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
'''Bakery Ruleset for nut plugin'''

# by Michael Kronika

#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  mk_puppet Plugin is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SingleChoice,
    SingleChoiceElement,
    DefaultValue,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic, Help


def _parameter_form_bakery() -> Dictionary:
    return Dictionary(
        elements={
            "deploy": DictElement(
                required=True,
                parameter_form=SingleChoice(
                    title=Title("Network UPS Tools agent plugin deployment"),
                    help_text=Help(
                        "Hosts configured via this rule get \
                        the <tt>NUT</tt> plugin"
                    ),
                    prefill=DefaultValue("yes"),
                    elements=[
                        SingleChoiceElement(
                            name="yes",
                            title=Title("Deploy the NUT plugin"),
                        ),
                        SingleChoiceElement(
                            name="no",
                            title=Title("Do not deploy NUT plugin"),
                        ),
                    ],
                ),
            )
        }
    )


rule_spec_bakery_nut = AgentConfig(
    name="nut",
    title=Title("Network UPS Tools agent plugin"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_bakery,
)
