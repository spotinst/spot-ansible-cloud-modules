from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import unittest
import sys
from mock import MagicMock
from ansible_collections.spot.cloud_modules.plugins.modules.azure_elastigroup import turn_to_model
from spotinst_sdk2.models.elastigroup.azure_v3 import (
    Capacity,
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
            'name': 'ansible-azure-elastigroup-example',
            'region': 'eastus',
            'resource_group_name': 'AutomationResourceGroup',
            'description': 'a sample Azure Elastigroup created via Ansible',
            'capacity': {
                'minimum': 2,
                'maximum': 6,
                'target': 4,
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
			        'type': 'scaleUp',
                    'adjustment': 2
		        }]
	        },
	        'strategy': {
		        'draining_timeout': 100,
		        'fallback_to_od': True,
		        'spot_percentage': 100,
		        'revert_to_spot': {
			        'perform_at': 'always'
		        },
		        'signals': [{
			        'timeout': 180,
			        'type': 'vmReady'
		        },
                {
			        'timeout': 210,
			        'type': 'vmReadyToShutdown'
		        }]
	        },
	        'compute': {
		        'os': 'Linux',
		        'zones': ['1', '2', '3'],
		        'preferred_zones': ['2'],
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
			        },
                    {
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
				        'size': 30,
				        'type': 'Standard_LRS'
			        },
			        'shutdown_script': 'VGhpcyBpcyBzaHV0ZG93biBzY3JpcHQ=',
			        'tags': [{
				        'tag_key': 'Creator',
				        'tag_value': 'Ansible Test'
			        },
                    {
				        'tag_key': 'Name',
				        'tag_value': 'Ansible Detailed Example'
			        }]
		        }
	        }
        }

        module = MockModule(input_dict=input_dict)
        eg = turn_to_model(module.params, "elastigroup")

        # test name
        self.assertEqual(eg.name, "ansible-azure-elastigroup-example")

        # test region
        self.assertEqual(eg.region, "eastus")

        # test resource group name
        self.assertEqual(eg.resource_group_name, "AutomationResourceGroup")

        # test description
        self.assertEqual(eg.description, "a sample Azure Elastigroup created via Ansible")

        # test persistence
        expected_capacity = Capacity(minimum=2, maximum=6, target=4)

        actual_capacity = eg.capacity

        self.assertEqual(actual_capacity.minimum, expected_capacity.minimum)
        self.assertEqual(actual_capacity.maximum, expected_capacity.maximum)
        self.assertEqual(actual_capacity.target, expected_capacity.target)

        # test health
        expected_health = Health(health_check_types=["vmState"], grace_period=300, unhealthy_duration=120, auto_healing=True)

        actual_health = eg.health

        self.assertEqual(actual_health.health_check_types, expected_health.health_check_types)
        self.assertEqual(actual_health.auto_healing, expected_health.auto_healing)
        self.assertEqual(actual_health.grace_period, expected_health.grace_period)
        self.assertEqual(actual_health.unhealthy_duration, expected_health.unhealthy_duration)

        # test scheduling
        expected_scheduling = Scheduling(tasks=[SchedulingTask(is_enabled=True, cron_expression="* * * 1 *", type="scaleUp", adjustment=2)])

        actual_scheduling = eg.scheduling
        self.assertEqual(len(actual_scheduling.tasks), len(expected_scheduling.tasks))

        self.assertEqual(actual_scheduling.tasks[0].is_enabled, expected_scheduling.tasks[0].is_enabled)
        self.assertEqual(actual_scheduling.tasks[0].cron_expression, expected_scheduling.tasks[0].cron_expression)
        self.assertEqual(actual_scheduling.tasks[0].type, expected_scheduling.tasks[0].type)
        self.assertEqual(actual_scheduling.tasks[0].adjustment, expected_scheduling.tasks[0].adjustment)

        # test strategy
        expected_strategy = Strategy(draining_timeout=100, fallback_to_od=True, spot_percentage=100,
                                     revert_to_spot=RevertToSpot(perform_at="always"),
                                     signals=[Signal(timeout=180, type="vmReady"), Signal(timeout=210, type="vmReadyToShutdown")])

        actual_strategy = eg.strategy

        self.assertEqual(actual_strategy.draining_timeout, expected_strategy.draining_timeout)
        self.assertEqual(actual_strategy.fallback_to_od, expected_strategy.fallback_to_od)
        self.assertEqual(actual_strategy.spot_percentage, expected_strategy.spot_percentage)
        self.assertEqual(actual_strategy.revert_to_spot.perform_at, expected_strategy.revert_to_spot.perform_at)

        self.assertEqual(len(actual_strategy.signals), len(expected_strategy.signals))

        self.assertEqual(actual_strategy.signals[0].timeout, expected_strategy.signals[0].timeout)
        self.assertEqual(actual_strategy.signals[0].type, expected_strategy.signals[0].type)

        self.assertEqual(actual_strategy.signals[1].timeout, expected_strategy.signals[1].timeout)
        self.assertEqual(actual_strategy.signals[1].type, expected_strategy.signals[1].type)

        # test compute
        self.assertEqual(eg.compute.os, "Linux")
        self.assertEqual(sorted(eg.compute.zones), sorted(["1", "2", "3"]))
        self.assertEqual(sorted(eg.compute.preferred_zones), sorted(["2"]))
        self.assertEqual(sorted(eg.compute.vm_sizes.od_sizes), sorted(['standard_a1_v2', 'standard_a2_v2']))
        self.assertEqual(sorted(eg.compute.vm_sizes.spot_sizes), sorted(['standard_a1_v2', 'standard_a2_v2']))
        self.assertEqual(sorted(eg.compute.vm_sizes.preferred_spot_sizes), sorted(['standard_a1_v2']))

        # test LaunchSpecification
        expected_boot_diagnostics = BootDiagnostics(is_enabled=True, type="managed")
        actual_boot_diagnostics = eg.compute.launch_specification.boot_diagnostics
        self.assertEqual(actual_boot_diagnostics.is_enabled, expected_boot_diagnostics.is_enabled)
        self.assertEqual(actual_boot_diagnostics.type, expected_boot_diagnostics.type)

        self.assertEqual(eg.compute.launch_specification.custom_data, "VGhpcyBpcyBjdXN0b20gZGF0YSBmaWVsZA==")

        expected_datadisks = [DataDisk(lun=0, size_g_b=30, type="Standard_LRS"),
                            DataDisk(lun=1, size_g_b=32, type="StandardSSD_LRS")]

        actual_datadisks = eg.compute.launch_specification.data_disks
        self.assertEqual(len(actual_datadisks), len(expected_datadisks))

        self.assertEqual(actual_datadisks[0].lun, expected_datadisks[0].lun)
        self.assertEqual(actual_datadisks[0].size_g_b, expected_datadisks[0].size_g_b)
        self.assertEqual(actual_datadisks[0].type, expected_datadisks[0].type)

        self.assertEqual(actual_datadisks[1].lun, expected_datadisks[1].lun)
        self.assertEqual(actual_datadisks[1].size_g_b, expected_datadisks[1].size_g_b)
        self.assertEqual(actual_datadisks[1].type, expected_datadisks[1].type)

        expected_marketplace = Marketplace(publisher="Canonical", offer="UbuntuServer", sku="18.04-LTS", version="latest")
        actual_marketplace = eg.compute.launch_specification.image.marketplace

        self.assertEqual(actual_marketplace.publisher, expected_marketplace.publisher)
        self.assertEqual(actual_marketplace.offer, expected_marketplace.offer)
        self.assertEqual(actual_marketplace.sku, expected_marketplace.sku)
        self.assertEqual(actual_marketplace.version, expected_marketplace.version)

        expected_login = Login(user_name="ubuntu", ssh_public_key="my-ssh-key")
        actual_login = eg.compute.launch_specification.login
        self.assertEqual(actual_login.user_name, expected_login.user_name)
        self.assertEqual(actual_login.ssh_public_key, expected_login.ssh_public_key)

        expected_network = Network(resource_group_name="AutomationResourceGroup",
                                   virtual_network_name="Automation-VirtualNetwork",
				                    network_interfaces=[NetworkInterface(is_primary=True, assign_public_ip=True, public_ip_sku="Standard", subnet_name="Automation-PrivateSubnet", enable_ip_forwarding=True)])

        actual_network = eg.compute.launch_specification.network

        self.assertEqual(actual_network.resource_group_name, expected_network.resource_group_name)
        self.assertEqual(actual_network.virtual_network_name, expected_network.virtual_network_name)
        self.assertEqual(len(actual_network.network_interfaces), len(expected_network.network_interfaces))
        self.assertEqual(actual_network.network_interfaces[0].is_primary, expected_network.network_interfaces[0].is_primary)
        self.assertEqual(actual_network.network_interfaces[0].assign_public_ip, expected_network.network_interfaces[0].assign_public_ip)
        self.assertEqual(actual_network.network_interfaces[0].public_ip_sku, expected_network.network_interfaces[0].public_ip_sku)
        self.assertEqual(actual_network.network_interfaces[0].subnet_name, expected_network.network_interfaces[0].subnet_name)
        self.assertEqual(actual_network.network_interfaces[0].enable_ip_forwarding, expected_network.network_interfaces[0].enable_ip_forwarding)

        expected_os_disk = OsDisk(size=30, type="Standard_LRS")
        actual_os_disk = eg.compute.launch_specification.os_disk
        self.assertEqual(actual_os_disk.size, expected_os_disk.size)
        self.assertEqual(actual_os_disk.type, expected_os_disk.type)

        self.assertEqual(eg.compute.launch_specification.shutdown_script, "VGhpcyBpcyBzaHV0ZG93biBzY3JpcHQ=")

        expected_tags = [Tag(tag_key="Creator", tag_value="Ansible Test"), Tag(tag_key="Name", tag_value="Ansible Detailed Example")]
        actual_tags = eg.compute.launch_specification.tags

        self.assertEqual(len(actual_tags), len(expected_tags))
        self.assertEqual(actual_tags[0].tag_key, expected_tags[0].tag_key)
        self.assertEqual(actual_tags[0].tag_value, expected_tags[0].tag_value)
        self.assertEqual(actual_tags[1].tag_key, expected_tags[1].tag_key)
        self.assertEqual(actual_tags[1].tag_value, expected_tags[1].tag_value)
