from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import unittest
import sys
from mock import MagicMock
from ansible_collections.spot.cloud_modules.plugins.modules.azure_stateful_node import turn_to_model
from spotinst_sdk2.models.stateful_node import (
    Persistence,
    Health,
    Scheduling,
    SchedulingTask,
    Strategy,
    Signal,
    RevertToSpot,
    BootDiagnostics,
    DataDisk,
    Marketplace,
    Login,
    Network,
    NetworkInterface,
    OsDisk,
    Tag
)

sys.modules['spotinst_sdk'] = MagicMock()


class MockModule:

    def __init__(self, input_dict):
        self.params = input_dict


class TestTurnToModel(unittest.TestCase):
    """Unit test for the turn to model helper function"""

    def test_all_fields(self):
        """Format input into proper json structure"""

        input_dict = {
            'name': 'ansible-stateful-node-example',
            'region': 'eastus',
            'resource_group_name': 'AutomationResourceGroup',
            'description': 'a sample Stateful Node created via Ansible',
            'persistence': {
                'data_disks_persistence_mode': 'reattach',
                'os_disk_persistence_mode': 'onlaunch',
                'should_persist_data_disks': True,
                'should_persist_network': True,
                'should_persist_os_disk': True
            },
            'health': {
                'health_check_types': ["vmState"],
                'grace_period': 300,
                'unhealthy_duration': 120,
                'auto_healing': True
            },
            'scheduling': {
                'tasks': [{
                    'is_enabled': True,
                    'cron_expression': '* * * 1 *',
                    'type': 'pause'
                }, {
                    'is_enabled': False,
                    'cron_expression': '* * * 3 *',
                    'type': 'resume'
                }]
            },
            'strategy': {
                'availability_vs_cost': 75,
                'draining_timeout': 100,
                'fallback_to_od': True,
                'preferred_lifecycle': 'spot',
                'revert_to_spot': {
                    'perform_at': 'always'
                },
                'signals': [{
                    'timeout': 180,
                    'type': 'vmReady'
                }, {
                    'timeout': 210,
                    'type': 'vmReadyToShutdown'
                }]
            },
            'compute': {
                'os': 'Linux',
                'zones': ["1", "2", "3"],
                'preferred_zone': '2',
                'vm_sizes': {
                    'od_sizes': ['standard_a1_v2', 'standard_a2_v2'],
                    'spot_sizes': ['standard_a1_v2', 'standard_a2_v2'],
                    'preferred_spot_sizes': ['standard_a1_v2']
                },
                'launch_specification': {
                    'boot_diagnostics': {
                        'is_enabled': True,
                        'type': 'managed'
                    },
                    'custom_data': 'VGhpcyBpcyBjdXN0b20gZGF0YSBmaWVsZA==',
                    'data_disks': [{
                        'lun': 0,
                        'size_g_b': 30,
                        'type': 'Standard_LRS'
                    }, {
                        'lun': 1,
                        'size_g_b': 32,
                        'type': 'StandardSSD_LRS'
                    }],
                    'image': {
                        'marketplace': {
                            'publisher': 'Canonical',
                            'version': 'latest',
                            'sku': '18.04-LTS',
                            'offer': 'UbuntuServer'
                        }
                    },
                    'login': {
                        'user_name': 'ubuntu',
                        'ssh_public_key': 'my-ssh-key'
                    },
                    'network': {
                        'resource_group_name': 'AutomationResourceGroup',
                        'virtual_network_name': 'Automation-VirtualNetwork',
                        'network_interfaces': [{
                            'is_primary': True,
                            'assign_public_ip': True,
                            'public_ip_sku': 'Standard',
                            'subnet_name': 'Automation-PrivateSubnet',
                            'enable_ip_forwarding': True
                        }]
                    },
                    'os_disk': {
                        'size_g_b': 30,
                        'type': 'Standard_LRS'
                    },
                    'shutdown_script': 'VGhpcyBpcyBzaHV0ZG93biBzY3JpcHQ=',
                    'tags': [{
                        'tag_key': 'Creator',
                        'tag_value': 'Ansible Test'
                    }, {
                        'tag_key': 'Name',
                        'tag_value': 'Ansible Detailed Example'
                    }]
                }
            }
        }

        module = MockModule(input_dict=input_dict)
        ssn = turn_to_model(module.params, "stateful_node")

        # test name
        self.assertEqual(ssn.name, "ansible-stateful-node-example")

        # test region
        self.assertEqual(ssn.region, "eastus")

        # test resource group name
        self.assertEqual(ssn.resource_group_name, "AutomationResourceGroup")

        # test description
        self.assertEqual(ssn.description, "a sample Stateful Node created via Ansible")

        # test persistence
        expected_persistence = Persistence(data_disks_persistence_mode='reattach',
                                           os_disk_persistence_mode='onlaunch',
                                           should_persist_data_disks=True,
                                           should_persist_network=True,
                                           should_persist_os_disk=True)

        actual_persistence = ssn.persistence

        self.assertEqual(actual_persistence.data_disks_persistence_mode, expected_persistence.data_disks_persistence_mode)
        self.assertEqual(actual_persistence.os_disk_persistence_mode, expected_persistence.os_disk_persistence_mode)
        self.assertEqual(actual_persistence.should_persist_data_disks, expected_persistence.should_persist_data_disks)
        self.assertEqual(actual_persistence.should_persist_network, expected_persistence.should_persist_network)
        self.assertEqual(actual_persistence.should_persist_os_disk, expected_persistence.should_persist_os_disk)

        # test health
        expected_health = Health(health_check_types=["vmState"], grace_period=300, unhealthy_duration=120, auto_healing=True)

        actual_health = ssn.health

        self.assertEqual(actual_health.health_check_types, expected_health.health_check_types)
        self.assertEqual(actual_health.auto_healing, expected_health.auto_healing)
        self.assertEqual(actual_health.grace_period, expected_health.grace_period)
        self.assertEqual(actual_health.unhealthy_duration, expected_health.unhealthy_duration)

        # test scheduling
        expected_scheduling = Scheduling(tasks=[SchedulingTask(is_enabled=True, cron_expression="* * * 1 *", type="pause"),
                                                SchedulingTask(is_enabled=False, cron_expression="* * * 3 *", type="resume")])

        actual_scheduling = ssn.scheduling
        self.assertEqual(len(actual_scheduling.tasks), len(expected_scheduling.tasks))

        self.assertEqual(actual_scheduling.tasks[0].is_enabled, expected_scheduling.tasks[0].is_enabled)
        self.assertEqual(actual_scheduling.tasks[0].cron_expression, expected_scheduling.tasks[0].cron_expression)
        self.assertEqual(actual_scheduling.tasks[0].type, expected_scheduling.tasks[0].type)

        self.assertEqual(actual_scheduling.tasks[1].is_enabled, expected_scheduling.tasks[1].is_enabled)
        self.assertEqual(actual_scheduling.tasks[1].cron_expression, expected_scheduling.tasks[1].cron_expression)
        self.assertEqual(actual_scheduling.tasks[1].type, expected_scheduling.tasks[1].type)

        # test strategy
        expected_strategy = Strategy(availability_vs_cost=75, draining_timeout=100, fallback_to_od=True, preferred_lifecycle="spot",
                                     revert_to_spot=RevertToSpot(perform_at="always"),
                                     signals=[Signal(timeout=180, type="vmReady"), Signal(timeout=210, type="vmReadyToShutdown")])

        actual_strategy = ssn.strategy

        self.assertEqual(actual_strategy.availability_vs_cost, expected_strategy.availability_vs_cost)
        self.assertEqual(actual_strategy.draining_timeout, expected_strategy.draining_timeout)
        self.assertEqual(actual_strategy.fallback_to_od, expected_strategy.fallback_to_od)
        self.assertEqual(actual_strategy.preferred_lifecycle, expected_strategy.preferred_lifecycle)
        self.assertEqual(actual_strategy.revert_to_spot.perform_at, expected_strategy.revert_to_spot.perform_at)

        self.assertEqual(len(actual_strategy.signals), len(expected_strategy.signals))

        self.assertEqual(actual_strategy.signals[0].timeout, expected_strategy.signals[0].timeout)
        self.assertEqual(actual_strategy.signals[0].type, expected_strategy.signals[0].type)

        self.assertEqual(actual_strategy.signals[1].timeout, expected_strategy.signals[1].timeout)
        self.assertEqual(actual_strategy.signals[1].type, expected_strategy.signals[1].type)

        # test compute
        self.assertEqual(ssn.compute.os, "Linux")
        self.assertEqual(sorted(ssn.compute.zones), sorted(["1", "2", "3"]))
        self.assertEqual(ssn.compute.preferred_zone, "2")
        self.assertEqual(sorted(ssn.compute.vm_sizes.od_sizes), sorted(['standard_a1_v2', 'standard_a2_v2']))
        self.assertEqual(sorted(ssn.compute.vm_sizes.spot_sizes), sorted(['standard_a1_v2', 'standard_a2_v2']))
        self.assertEqual(sorted(ssn.compute.vm_sizes.preferred_spot_sizes), sorted(['standard_a1_v2']))

        # test LaunchSpecification
        expected_boot_diagnostics = BootDiagnostics(is_enabled=True, type="managed")
        actual_boot_diagnostics = ssn.compute.launch_specification.boot_diagnostics
        self.assertEqual(actual_boot_diagnostics.is_enabled, expected_boot_diagnostics.is_enabled)
        self.assertEqual(actual_boot_diagnostics.type, expected_boot_diagnostics.type)

        self.assertEqual(ssn.compute.launch_specification.custom_data, "VGhpcyBpcyBjdXN0b20gZGF0YSBmaWVsZA==")

        expected_datadisks = [DataDisk(lun=0, size_g_b=30, type="Standard_LRS"),
                              DataDisk(lun=1, size_g_b=32, type="StandardSSD_LRS")]

        actual_datadisks = ssn.compute.launch_specification.data_disks
        self.assertEqual(len(actual_datadisks), len(expected_datadisks))

        self.assertEqual(actual_datadisks[0].lun, expected_datadisks[0].lun)
        self.assertEqual(actual_datadisks[0].size_g_b, expected_datadisks[0].size_g_b)
        self.assertEqual(actual_datadisks[0].type, expected_datadisks[0].type)

        self.assertEqual(actual_datadisks[1].lun, expected_datadisks[1].lun)
        self.assertEqual(actual_datadisks[1].size_g_b, expected_datadisks[1].size_g_b)
        self.assertEqual(actual_datadisks[1].type, expected_datadisks[1].type)

        expected_marketplace = Marketplace(publisher="Canonical", offer="UbuntuServer", sku="18.04-LTS", version="latest")
        actual_marketplace = ssn.compute.launch_specification.image.marketplace

        self.assertEqual(actual_marketplace.publisher, expected_marketplace.publisher)
        self.assertEqual(actual_marketplace.offer, expected_marketplace.offer)
        self.assertEqual(actual_marketplace.sku, expected_marketplace.sku)
        self.assertEqual(actual_marketplace.version, expected_marketplace.version)

        expected_login = Login(user_name="ubuntu", ssh_public_key="my-ssh-key")
        actual_login = ssn.compute.launch_specification.login
        self.assertEqual(actual_login.user_name, expected_login.user_name)
        self.assertEqual(actual_login.ssh_public_key, expected_login.ssh_public_key)

        expected_network = Network(resource_group_name="AutomationResourceGroup",
                                   virtual_network_name="Automation-VirtualNetwork",
                                   network_interfaces=[NetworkInterface(is_primary=True, assign_public_ip=True, public_ip_sku="Standard",
                                                                        subnet_name="Automation-PrivateSubnet", enable_ip_forwarding=True)])

        actual_network = ssn.compute.launch_specification.network

        self.assertEqual(actual_network.resource_group_name, expected_network.resource_group_name)
        self.assertEqual(actual_network.virtual_network_name, expected_network.virtual_network_name)
        self.assertEqual(len(actual_network.network_interfaces), len(expected_network.network_interfaces))
        self.assertEqual(actual_network.network_interfaces[0].is_primary, expected_network.network_interfaces[0].is_primary)
        self.assertEqual(actual_network.network_interfaces[0].assign_public_ip, expected_network.network_interfaces[0].assign_public_ip)
        self.assertEqual(actual_network.network_interfaces[0].public_ip_sku, expected_network.network_interfaces[0].public_ip_sku)
        self.assertEqual(actual_network.network_interfaces[0].subnet_name, expected_network.network_interfaces[0].subnet_name)
        self.assertEqual(actual_network.network_interfaces[0].enable_ip_forwarding, expected_network.network_interfaces[0].enable_ip_forwarding)

        expected_os_disk = OsDisk(size_g_b=30, type="Standard_LRS")
        actual_os_disk = ssn.compute.launch_specification.os_disk
        self.assertEqual(actual_os_disk.size_g_b, expected_os_disk.size_g_b)
        self.assertEqual(actual_os_disk.type, expected_os_disk.type)

        self.assertEqual(ssn.compute.launch_specification.shutdown_script, "VGhpcyBpcyBzaHV0ZG93biBzY3JpcHQ=")

        expected_tags = [Tag(tag_key="Creator", tag_value="Ansible Test"), Tag(tag_key="Name", tag_value="Ansible Detailed Example")]
        actual_tags = ssn.compute.launch_specification.tags

        self.assertEqual(len(actual_tags), len(expected_tags))
        self.assertEqual(actual_tags[0].tag_key, expected_tags[0].tag_key)
        self.assertEqual(actual_tags[0].tag_value, expected_tags[0].tag_value)
        self.assertEqual(actual_tags[1].tag_key, expected_tags[1].tag_key)
        self.assertEqual(actual_tags[1].tag_value, expected_tags[1].tag_value)
