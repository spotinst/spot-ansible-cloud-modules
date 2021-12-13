from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule


class SpotAnsibleModule(AnsibleModule):

    def __init__(self, argument_spec, bypass_checks=False, no_log=False, mutually_exclusive=None,
                 required_together=None, required_one_of=None, add_file_common_args=False, supports_check_mode=False,
                 required_if=None, required_by=None):
        """
        Common code for quickly building an ansible module in Python
        (although you can write modules with anything that can return JSON).

        See :ref:`developing_modules_general` for a general introduction
        and :ref:`developing_program_flow_modules` for more detailed explanation.
        """

        self.argument_spec = argument_spec

        self._load_params()
        self._set_internal_properties()
        self.custom_params = self.params
        super().__init__(argument_spec, bypass_checks, no_log, mutually_exclusive, required_together, required_one_of,
                         add_file_common_args, supports_check_mode, required_if, required_by)
