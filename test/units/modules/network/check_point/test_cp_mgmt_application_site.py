# Ansible module to manage CheckPoint Firewall (c) 2019
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
from units.modules.utils import set_module_args, exit_json, fail_json, AnsibleFailJson, AnsibleExitJson

from ansible.module_utils import basic
from ansible.modules.network.check_point import cp_mgmt_application_site

OBJECT = {
    "name": "New Application Site 1",
    "description": "My Application Site",
    "primary_category": "Social Networking",
    "additional_categories": [
        "Instant Chat",
        "Supports Streaming",
        "New Application Site Category 1"
    ],
    "url_list": [
        "www.cnet.com",
        "www.stackoverflow.com"
    ],
    "urls_defined_as_regular_expression": False
}

CREATE_PAYLOAD = {
    "name": "New Application Site 1",
    "description": "My Application Site",
    "primary_category": "Social Networking",
    "additional_categories": [
        "Instant Chat",
        "Supports Streaming",
        "New Application Site Category 1"
    ],
    "url_list": [
        "www.cnet.com",
        "www.stackoverflow.com"
    ],
    "urls_defined_as_regular_expression": False
}

UPDATE_PAYLOAD = {
    "name": "New Application Site 1",
    "description": "My New Application Site",
    "primary_category": "Instant Chat",
    "urls_defined_as_regular_expression": True
}

DELETE_PAYLOAD = {
    "name": "New Application Site 1",
    "state": "absent"
}

function_path = 'ansible.modules.network.check_point.cp_mgmt_application_site.api_call'
api_call_object = 'application_site'


class TestCheckpointApplicationSite(object):
    module = cp_mgmt_application_site

    @pytest.fixture(autouse=True)
    def module_mock(self, mocker):
        return mocker.patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)

    @pytest.fixture
    def connection_mock(self, mocker):
        connection_class_mock = mocker.patch('ansible.module_utils.network.checkpoint.checkpoint.Connection')
        return connection_class_mock.return_value

    def test_create(self, mocker, connection_mock):
        mock_function = mocker.patch(function_path)
        mock_function.return_value = {'changed': True, api_call_object: OBJECT}
        connection_mock.api_call.return_value = {'changed': True, api_call_object: OBJECT}
        result = self._run_module(CREATE_PAYLOAD)

        assert result['changed']
        assert api_call_object in result

    def test_create_idempotent(self, mocker, connection_mock):
        mock_function = mocker.patch(function_path)
        mock_function.return_value = {'changed': False, api_call_object: OBJECT}
        connection_mock.send_request.return_value = (200, OBJECT)
        result = self._run_module(CREATE_PAYLOAD)

        assert not result['changed']

    def test_update(self, mocker, connection_mock):
        mock_function = mocker.patch(function_path)
        mock_function.return_value = {'changed': True, api_call_object: OBJECT}
        connection_mock.send_request.return_value = (200, OBJECT)
        result = self._run_module(UPDATE_PAYLOAD)

        assert result['changed']

    def test_update_idempotent(self, mocker, connection_mock):
        mock_function = mocker.patch(function_path)
        mock_function.return_value = {'changed': False, api_call_object: OBJECT}
        connection_mock.send_request.return_value = (200, OBJECT)
        result = self._run_module(UPDATE_PAYLOAD)

        assert not result['changed']

    def test_delete(self, mocker, connection_mock):
        mock_function = mocker.patch(function_path)
        mock_function.return_value = {'changed': True}
        connection_mock.send_request.return_value = (200, OBJECT)
        result = self._run_module(DELETE_PAYLOAD)

        assert result['changed']

    def test_delete_idempotent(self, mocker, connection_mock):
        mock_function = mocker.patch(function_path)
        mock_function.return_value = {'changed': False}
        connection_mock.send_request.return_value = (200, OBJECT)
        result = self._run_module(DELETE_PAYLOAD)

        assert not result['changed']

    def _run_module(self, module_args):
        set_module_args(module_args)
        with pytest.raises(AnsibleExitJson) as ex:
            self.module.main()
        return ex.value.args[0]
