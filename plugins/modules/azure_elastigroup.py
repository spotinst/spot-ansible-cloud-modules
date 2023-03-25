#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: azure_elastigroup
version_added: 1.2.0
short_description: Create, update or delete Spot Azure Elastigroup
author: Spot by NetApp (@anuragsharma-123)
description: >
    Create, update, delete or perform actions (pause, resume, recyce) on Spot Azure Stateful Nodes.
    You will have to have a credentials file in this location - <home>/.spotinst/credentials
    The credentials file must contain a row that looks like this
    token = <YOUR TOKEN>
    Full documentation available at [our docs site](https://docs.spot.io/)
extends_documentation_fragment:
  - spot.cloud_modules.requirements
options:
    token:
        type: str
        description:
            - "Optional parameter that allows to set an token inside the module configuration. By default this is retrieved from the credentials path"
    credentials_path:
        type: str
        default: "/root/.spotinst/credentials"
        description: "Optional parameter that allows to set a non-default credentials path."
    state:
        type: str
        choices:
            - present
            - absent
        default: present
        description: "create update or delete"
    account_id:
        type: str
        description:
            - "Optional parameter that allows to set an account-id inside the module configuration. By default this is retrieved from the credentials path"
    id:
        type: str
        description:
            - "Azure Elastigroup ID."
            - "This will have no effect unless the `uniqueness_by` field is set to ID."
            - "When this is set, and the `uniqueness_by` field is set, the group will either be updated or deleted, but not created."
    uniqueness_by:
        type: str
        choices:
            - id
            - name
        description:
            - "If your Stateful Node names are not unique, you may use this feature to update or delete a specific node."
            - "Whenever this property is set, you must set a an `id` in order to update or delete elastigroup, otherwise elastigroup node will be created."
    do_not_update:
        type: list
        elements: str
        description:
            - "A list of dotted paths to attributes that you don't wish to update during an update operation."
            - "Example: Specifying `compute.product` will make sure that this attribute is never updated."
    elastigroup:
        type: dict
        description: "Describe the desired properties of the azure elastigroup under this object."
        suboptions:
            name:
                type: str
                description: "The stateful node's name."
                required: true
            region:
                type: str
                description: "The Azure region in which the Stateful Node will be launched."
                required: true
            resource_group_name:
                type: str
                description: "The Azure resource group in which the VM and all of the subsequent subresources will be launched."
                required: true
            description:
                type: str
                description: "optional description for the stateful node."
            capacity:
                type: dict
                description: Capacity of Elastigroup.
                suboptions:
                    maximum:
                        type: int
                        description: "The Elastigroup will not set a target greater than this value"
                    minimum:
                        type: int
                        description: "The Elastigroup will not set a target below this value"
                    target:
                        type: int
                        description: "Current scale the Elastigroup will conform to"
            health:
                type: dict
                description: "Set health check and auto-healing of unhealthy VMs."
                suboptions:
                    health_check_types:
                        type: str
                        description: "Health check types to use in order to validate VM health."
                    auto_healing:
                        type: bool
                        description: "Enable auto-healing of unhealthy VMs."
                    grace_period:
                        type: int
                        description: "The amount of time (in seconds) after a new VM has launched before terminating the old VM."
                    unhealthy_duration:
                        type: int
                        description: "Amount of time (in seconds) for the VM to remain unhealthy before a replacement is triggered."
            scheduling:
                type: dict
                description: "Define cron-based scheduled tasks."
                suboptions:
                    tasks:
                        type: list
                        elements: dict
                        description: "A list of scheduling tasks."
                        suboptions:
                            type:
                                type: str
                                description: "Define cron-based scheduled tasks. valid values: `scale`, `scaleUp`, `scaleDown`
                                `scaleUpPercentage`, `scaleDownPercentage` and `deployment`"
                            cron_expression:
                                type: str
                                description: "A valid cron expression that describes the scheduled task (UTC)."
                            is_enabled:
                                type: bool
                                description: "Describes whether the task is enabled. When true the task should run when false it should not run."
                            start_time:
                                type: str
                                description: "Start Time."
                            frequency:
                                type: str
                                description: "Frequency."                                
                            scale_target_capacity:
                                type: int
                                description: "This will set the defined target group capacity when the scheduling task is triggered."
                            scale_min_capacity:
                                type: int
                                description: "This will set the defined maximum group capacity when the scheduling task is triggered."
                            scale_max_capacity:
                                type: int
                                description: "This will set the defined maximum group capacity when the scheduling task is triggered."            
                            batch_size_percentage:
                                type: int
                                description: "Indicates the timeout (in seconds) to wait until the VM becomes healthy, based on the healthCheckType."
                            grace_period:
                                type: str
                                description: "Indicates (in seconds) the timeout to wait until instance become healthy based on the healthCheckType."
                            adjustment:
                                type: str
                                description: "This will decrease the target capacity by the defined amount when the scheduling task is triggered."                                
                            adjustment_percentage:
                                type: int
                                description: "This will decrease the target capacity by the defined percentage value when the scheduling task is triggered."
                            target_capacity:
                                type: int
                                description: "This will set the defined target group capacity when the scheduling task is triggered."
                            min_capacity:
                                type: int
                                description: "This will set the defined maximum group capacity when the scheduling task is triggered." 
                            max_capacity:
                                type: int
                                description: "This will set the defined maximum group capacity when the scheduling task is triggered."
            scaling:
                type: dict
                description: "Scaling Policies for Elastigroup."
                suboptions:
                    down:
                        type: list
                        elements: dict
                        description: "Defines scaling down policy."
                        suboptions:
                            action:
                                type: dict
                                description: "Scaling action to take when the policy is triggered."
                                suboptions:
                                    adjustment:
                                        type: str
                                        description: "Value to which the action type will be adjusted. Required if using `adjustment` action type."
                                    maximum:
                                        type: int
                                        description: "Value to update the group maximum capacity to. Required if using `updateCapacity` as action type."
                                    minimum:
                                        type: int
                                        description: "Value to update the group minimum capacity to. Required if using `updateCapacity` as action type."
                                    target:
                                        type: int
                                        description: "Value to update the group target capacity to. Required if using `updateCapacity` as action type."
                                    type:
                                        type: str
                                        description: "Type of scaling action to take when the scaling policy is triggered. 
                                        valid values: `adjustment` and `updateCapacity`"
                            cooldown:
                                type: int
                                description: "Time (seconds) to wait after a scaling action before resuming monitoring."
                            dimensions:
                                type: list
                                elements: dict
                                description: "Required if scaling.up.namespace is different from `Microsoft.Compute`."
                                suboptions:
                                    name:
                                        type: str
                                        description: "Dimension Name"
                                    value:
                                        type: str
                                        description: "Dimension Value"
                            evaluation_periods:
                                type: int
                                description: "Number of consecutive periods in which the threshold must be met in order to trigger the scaling action."
                            metric_name:
                                type: str
                                description: "Metric to monitor by Azure metric display name"
                            namespace:
                                type: str
                                description: "Namespace"
                            operator:
                                type: str
                                description: "The operator used to evaluate the threshold against the current metric value. 
                                valid values: `gt`, `gte`, `lt`, `lte`"
                            period:
                                type: int
                                description: "Amount of time (seconds) for which the threshold must be met in order to trigger the scaling action. 
                                valid values: 60, 300, 900, 1800, 3600, 7200"
                            policy_name:
                                type: str
                                description: "Name of scaling policy." 
                            statistic:
                                type: str
                                description: "Statistic by which to evaluate the selected metric.
                                valid values: `average`, `total`, `minimum`, `maximum`, `count`"                               
                            threshold:
                                type: float
                                description: "The value at which the scaling action is triggered."
                            unit:
                                type: str
                                description: "Unit to measure to evaluate the selected metric."
                    up:
                        type: list
                        elements: dict
                        description: "Defines scaling up policy."
                        suboptions:
                            action:
                                type: dict
                                description: "Scaling action to take when the policy is triggered."
                                suboptions:
                                    adjustment:
                                        type: str
                                        description: "Value to which the action type will be adjusted. Required if using `adjustment` action type."
                                    maximum:
                                        type: int
                                        description: "Value to update the group maximum capacity to. Required if using `updateCapacity` as action type."
                                    minimum:
                                        type: int
                                        description: "Value to update the group minimum capacity to. Required if using `updateCapacity` as action type."
                                    target:
                                        type: int
                                        description: "Value to update the group target capacity to. Required if using `updateCapacity` as action type."
                                    type:
                                        type: str
                                        description: "Type of scaling action to take when the scaling policy is triggered. 
                                        valid values: `adjustment` and `updateCapacity`"
                            cooldown:
                                type: int
                                description: "Time (seconds) to wait after a scaling action before resuming monitoring."
                            dimensions:
                                type: list
                                elements: dict
                                description: "Required if scaling.up.namespace is different from "Microsoft.Compute"."
                                suboptions:
                                    name:
                                        type: str
                                        description: "Dimension Name"
                                    value:
                                        type: str
                                        description: "Dimension Value"
                            evaluation_periods:
                                type: int
                                description: "Number of consecutive periods in which the threshold must be met in order to trigger the scaling action."
                            metric_name:
                                type: str
                                description: "Metric to monitor by Azure metric display name"
                            namespace:
                                type: str
                                description: "Namespace"
                            operator:
                                type: str
                                description: "The operator used to evaluate the threshold against the current metric value. 
                                valid values: `gt`, `gte`, `lt`, `lte`"
                            period:
                                type: int
                                description: "Amount of time (seconds) for which the threshold must be met in order to trigger the scaling action. 
                                valid values: 60, 300, 900, 1800, 3600, 7200"
                            policy_name:
                                type: str
                                description: "Name of scaling policy." 
                            statistic:
                                type: str
                                description: "Statistic by which to evaluate the selected metric.
                                valid values: `average`, `total`, `minimum`, `maximum`, `count`"                               
                            threshold:
                                type: float
                                description: "The value at which the scaling action is triggered."
                            unit:
                                type: str
                                description: "Unit to measure to evaluate the selected metric."         
            strategy:
                type: dict
                description: "Strategy for Elastigroup."
                suboptions:
                    draining_timeout:
                        type: int
                        description: "Time (seconds) to allow the VM be drained from incoming TCP connections and detached from MLB before 
                        terminating it during a scale down operation. Default: 120."
                    fallback_to_od:
                        type: bool
                        description: "In case of no spots available, elastigroup will launch an On-demand instance instead"
                    on_demand_count:
                        type: int
                        description: "Percentage of Spot-VMs to maintain. Required if spotPercentage isn't specified."
                    optimization_windows:
                        type: list
                        elements: str
                        description: "When performAt is `timeWindow`: must specify a list of `timeWindows` with at least one time window Each string
                          is in theformat of - `ddd:hh:mm-ddd:hh:mm ddd` = day of week = Sun | Mon | Tue | Wed | Thu | Fri | Sat hh = hour 24 = 0 - 23
                            mm = minute = 0 - 59"
                    orientation:
                        type: str
                        description: "Specify the prediction algorithm strategy. valid values: `availability`, `cost`, `cheapest`"
                    revert_to_spot:
                        type: dict
                        description: "Hold settings for strategy correction - replacing On-Demand for Spot VMs."
                        suboptions:
                            perform_at:
                                type: str
                                description: "Settings for maintenance strategy. valid values: `always`, `never`, `timeWindow`. Default: `always`"
                    signals:
                        type: list
                        elements: dict
                        description: Signals that VMs are expected to send to the platform.
                        suboptions:
                            timeout:
                                type: int
                                description: "The timeout in seconds to hold the vm until a signal is sent. Default: 1800"
                            type:
                                type: str
                                description: "The defined type of signal. Valid values: `vmReady`, `vmReadyToShutdown`"
                    spot_percentage:
                        type: int
                        description: "Percentage of Spot-VMs to maintain. Required if `od_count` isn't specified. default: 100"
            compute:
                type: dict
                description: "Defines the computational parameters to use when launch the VM for the Stateful Node."
                suboptions:
                    os:
                        type: str
                        description: "Defines the type of the operating system. Valid Values: `Linux`, `Windows`"
                    zones:
                        type: list
                        elements: str
                        description: "List of Azure Availability Zones in the defined region. Valid Values: `1`, `2`, `3`"
                    preferred_zones:
                        type: list
                        elements: str
                        description: "The AZs to prioritize when launching VMs. Must be a sublist of compute.zones"
                    vm_sizes:
                        type: dict
                        description: "Sizes of On-Demand and Low-Priority VMs."
                        suboptions:
                            od_sizes:
                                type: list
                                elements: str
                                description: "Defines the on-demand sizes to use when launching VMs."
                            spot_sizes:
                                type: list
                                elements: str
                                description: "Defines the spot-VM sizes to use when launching VMs."
                            preferred_spot_sizes:
                                type: list
                                elements: str
                                description: "Prioritize Spot VM sizes when launching Spot VMs. Must be a sublist of compute.vmSizes.spotSizes."
                    launch_specification:
                        type: dict
                        description: "Defines the launch specification of the VM."
                        suboptions:
                            boot_diagnostics:
                                type: dict
                                description: "Will enable boot diagnostics in Azure when a new VM is launched"
                                suboptions:
                                    is_enabled:
                                        type: bool
                                        description: "Allows you to enable and disable the configuration of boot diagnostics at launch"
                                    storage_uri:
                                        type: str
                                        description: "The storage URI that is used if a type is unmanaged."
                                    type:
                                        type: str
                                        description: "Defines the storage type on VM launch in Azure. Valid Values: `managed`, `unmanaged`"
                            custom_data:
                                type: str
                                description: "This value will hold the YML in base64 and will be added to the scaleSets."
                            data_disks:
                                type: list
                                elements: dict
                                description: "List of data disks to be attached to the vms in the group."
                                suboptions:
                                    lun:
                                        type: str
                                        description: "The LUN of the data disk."
                                    size_g_b:
                                        type: int
                                        description: "The size of the data disk in GB, required if dataDisks is specified."
                                    type:
                                        type: str
                                        description: "Type of data disk. Valid Values: `Standard_LRS`, `Premium_LRS`, `StandardSSD_LRS`, `UltraSSD_LRS`"
                            extensions:
                                type: list
                                elements: dict
                                description: "A list of objects for Azure extensions."
                                suboptions:
                                    api_version:
                                        type: str
                                        description: "The API version of the extension. Required if extension specified."
                                    auto_upgrade_minor_version:
                                        type: bool
                                        description: "Required on compute.launchSpecification.extensions object"
                                    minor_version_auto_upgrade:
                                        type: bool
                                        description: "Enable minor version upgrades of the extension. Required if extension specified."
                                    name:
                                        type: str
                                        description: "Required on compute.launchSpecification.extensions object"
                                    publisher:
                                        type: str
                                        description: "Required on compute.launchSpecification.extensions object"
                                    type:
                                        type: str
                                        description: "Required on compute.launchSpecification.extensions object"
                            image:
                                type: dict
                                description: "Defines the image with which the VM will be launched."
                                suboptions:
                                    custom:
                                        type: dict
                                        description: "Custom image definitions."
                                        suboptions:
                                            name:
                                                type: str
                                                description: "The name of the custom image."
                                            resource_group_name:
                                                type: str
                                                description: "The resource group name for custom image."
                                    gallery:
                                        type: dict
                                        description: "Gallery image definitions."
                                        suboptions:
                                            gallery_name:
                                                type: str
                                                description: "Name of the gallery."
                                            image_name:
                                                type: str
                                                description: "Name of the gallery image."
                                            resource_group_name:
                                                type: str
                                                description: "The resource group name for gallery image."
                                            spot_account_id:
                                                type: str
                                                description: "The Spot account ID that connected to the Azure subscription to which the gallery belongs."
                                            version:
                                                type: str
                                                description: "Image's version. Can be in the format x.x.x or 'latest'."
                                    marketplace:
                                        type: dict
                                        description: "Select an image from Azure's Marketplace image catalogue."
                                        suboptions:
                                            offer:
                                                type: str
                                                description: "Image offer."
                                            publisher:
                                                type: str
                                                description: "Image publisher."
                                            sku:
                                                type: str
                                                description: "Image Stock Keeping Unit, which is the specific version of the image."
                                            version:
                                                type: str
                                                description: "Image Version. Default: `latest`"
                            load_balancers_config:
                                type: dict
                                description: "Configure a Load Balancer."
                                suboptions:
                                    load_balancers:
                                        type: list
                                        elements: dict
                                        description: "Add a load balancer. For Azure Gateway, each Backend Pool is a separate load balancer."
                                        suboptions:
                                            application_gateway_name:
                                                type: str
                                                description: "Application Gateway Name"
                                            backend_pool_name:
                                                type: str
                                                description: "Name of the Backend Pool to register the group to."
                                            resource_group_name:
                                                type: str
                                                description: "The Resource Group name of the Load Balancer."
                                            type:
                                                type: str
                                                description: "The type of load balancer. Valid Values: `loadBalancer`, `applicationGateway`"
                                            auto_weight:
                                                type: boolean
                                                description:
                                                    - "auto weight"
                                            balancer_id:
                                                type: boolean
                                                description:
                                                    - "ID of Load Balancer"
                                            target_set_id:
                                                type: boolean
                                                description:
                                                    - "Target Set ID"
                            login:
                                type: dict
                                description: "Specify the authentication details to be used for launching VMs."
                                suboptions:
                                    password:
                                        type: str
                                        description: "Password for admin access to Windows VMs."
                                    ssh_public_key:
                                        type: str
                                        description: "SSH for admin access to Linux VMs."
                                    user_name:
                                        type: str
                                        description: "Defines the admin user name for launching VMs."
                            managed_service_identities:
                                type: list
                                elements: dict
                                description: "Add a user-assigned managed identity to the VMs in the cluster."
                                suboptions:
                                    resource_group_name:
                                        type: str
                                        description: "The Resource Group that the user-assigned managed identity resides in."
                                    name:
                                        type: str
                                        description: "Name of the managed identity."
                            network:
                                type: dict
                                description: "Define the Virtual Network and Subnet for your Elastigroup."
                                suboptions:
                                    resource_group_name:
                                        type: str
                                        description: "Defines the resource group name of the virtual network with which the VMs will be launched."
                                    virtual_network_name:
                                        type: str
                                        description: "Defines the name of the virtual network with which the VM will be launched."
                                    network_interfaces:
                                        type: list
                                        elements: dict
                                        description: "Defines the network interfaces with which the VM will be launched."
                                        suboptions:
                                            additional_ip_configurations:
                                                type: list
                                                elements: dict
                                                description: "Defines a list of extra IPs to be dynamically allocated."
                                                suboptions:
                                                    private_ip_address_version:
                                                        type: str
                                                        description: "Defines the version of the private IP address. Valid Values: `IPv4`, `IPv6`"
                                                    name:
                                                        type: str
                                                        description: "The name of the additional Ip Configuration."
                                            application_security_groups:
                                                type: list
                                                elements: dict
                                                description:
                                                    - Defines the Application Security Groups that will be associated to the primary IP configration
                                                      of the network interface.
                                                suboptions:
                                                    resource_group_name:
                                                        type: str
                                                        description: "Specify the resource group of the Application Security Group."
                                                    name:
                                                        type: str
                                                        description: "Specify the name of the Application Security Group."
                                            assign_public_ip:
                                                type: bool
                                                description: "Defines if a Public IP should be assigned in this network interface."
                                            enable_ip_forwarding:
                                                type: bool
                                                description: "Enables IP forwarding on the network interface."
                                            is_primary:
                                                type: bool
                                                description: "Defines whether the network interface is primary or not."
                                            security_group:
                                                type: dict
                                                description: "Defines the network security group to which the network interface will be assigned."
                                                suboptions:
                                                    resource_group_name:
                                                        type: str
                                                        description: "Specify the resource group of the security group."
                                                    name:
                                                        type: str
                                                        description: "Specify the name of the security group to use in this network interface."
                                            private_ip_addresses:
                                                type: list
                                                elements: str
                                                description: "Specify the private IP pool in which the VMs will be launched."
                                            public_ips:
                                                type: list
                                                elements: dict
                                                description: "Defined a pool of Public Ips (from Azure), that will be associated to the network interface."
                                                suboptions:
                                                    resource_group_name:
                                                        type: str
                                                        description: "Specify the resource group of the public IP."
                                                    name:
                                                        type: str
                                                        description: "Specify the name of the public IP to which the VMs will be assigned."
                                            public_ip_sku:
                                                type: str
                                                description: "Defines the type of public IP to assign the VM. Required if assignPublicIp=true. Valid Values: `Standard`, `Basic`"
                                            subnet_name:
                                                type: str
                                                description: "Defines the subnet to which the network interface will be connected."
                            os_disk:
                                type: dict
                                description: "Specify OS disk specification other than default."
                                suboptions:
                                    size:
                                        type: int
                                        description: "The size of the OS disk in GB."
                                    type:
                                        type: str
                                        description: "Type of OS disk. Valid Values: `Standard_LRS`, `Premium_LRS`, `StandardSSD_LRS`"
                            secrets:
                                type: list
                                elements: dict
                                description: "Set of certificates that should be installed on the VM"
                                suboptions:
                                    source_vault:
                                        type: dict
                                        description: "The key vault reference, contains the required certificates"
                                        suboptions:
                                            name:
                                                type: str
                                                description: "The name of the key vault"
                                            resource_group_name:
                                                type: str
                                                description: "The resource group name of the key vault"
                                    vault_certificates:
                                        type: list
                                        elements: dict
                                        description: "The required certificate references"
                                        suboptions:
                                            certificate_store:
                                                type: str
                                                description: "The certificate store directory the VM."
                                            certificate_url:
                                                type: str
                                                description: "The URL of the certificate under the key vault"
                            shutdown_script:
                                type: str
                                description: "Shutdown script for the group. Value should be passed as a string encoded at Base64 only."
                            tags:
                                description: "Defines the tags (unique key-value pairs) to tag your resources."
                                type: list
                                elements: dict
                                suboptions:
                                    tag_key:
                                        type: str
                                        description: "Tag Key for Vms in Elastigroup."
                                    tag_value:
                                        type: str
                                        description: "Tag Value for VMs in Elastigroup."
                            vm_name_prefix:
                                type: str
                                description: "Set a VM name prefix to be used for all launched VMs and the VM resources."
"""

EXAMPLES = """
# Basic Example
- hosts: localhost
  tasks:
    - name: azure_elastigroup_sample
      spot.cloud_modules.azure_elastigroup:
        state: present
        uniqueness_by: "id"
        do_not_update:
          - region
          - resource_group_name
          - compute.os
        elastigroup:
          name: "ansible-azure-elastigroup-example"
          description: "a sample Azure Elastigroup created via Ansible"
          region: "eastus"
          resource_group_name: "AutomationResourceGroup"
          capacity:
            minimum: 2
            maximum: 2
            target: 2
          health:
            health_check_types: ["vmState"]
            auto_healing: false
            grace_period: 300
            unhealthy_duration: 120           
          scheduling:
            tasks:
              - is_enabled: true
                cron_expression: "* * * 1 *"
                type: "scaleUp"
                adjustment: 2
          strategy:
            draining_timeout: 300
            fallback_to_od: true
            revert_to_spot:
              perform_at: "always"
            spot_percentage: 100
            signals:
              - timeout: 180
                type: "vmReady"
              - timeout: 210
                type: "vmReadyToShutdown"  
          compute:
            os: "Linux"
            zones: ["1", "2", "3"]
            preferred_zones: ["1", "2"]
            vm_sizes: 
              od_sizes: ["standard_ds1_v2", "standard_ds2_v2"]
              spot_sizes: ["standard_ds1_v2", "standard_ds2_v2"]
              preferred_spot_sizes: ["standard_ds1_v2"]
            launch_specification:
              data_disks:
                - lun: 0
                  size_g_b: 30
                  type: "Standard_LRS"
              image:
                marketplace:
                  publisher: "Canonical"
                  version: "latest"
                  sku: "18.04-LTS"
                  offer: "UbuntuServer"
              login:
                user_name: "ubuntu"
                ssh_public_key: <add-your-ssh-key-here>
              network:
                resource_group_name: "AutomationResourceGroup"
                virtual_network_name: "Automation-VirtualNetwork"
                network_interfaces:
                  - is_primary: true
                    assign_public_ip: true
                    public_ip_sku: "Standard"
                    subnet_name: "Automation-PrivateSubnet"
                    enable_ip_forwarding: true
              os_disk:
                size: 30
                type: "Standard_LRS"
              shutdown_script: "VGhpcyBpcyBzaHV0ZG93biBzY3JpcHQ="
              tags:
                - tag_key: "Creator"
                  tag_value: "Ansible Test"
      register: result
    - debug: var=result
"""

RETURN = """
---
group_id:
    description: The ID of the azure elastigroup that was just created/update/deleted.
    returned: success
    type: str
    sample: sig-15b1a394
"""

HAS_SPOTINST_SDK = False
HAS_ANSIBLE_MODULE = False


from ansible.module_utils.basic import AnsibleModule, env_fallback

try:
    from ..module_utils.spot_ansible_module import SpotAnsibleModule
    import copy
    import json

    HAS_ANSIBLE_MODULE = True

except ImportError as e:
    pass

try:
    import spotinst_sdk2 as spotinst
    from spotinst_sdk2.client import SpotinstClientException

    HAS_SPOTINST_SDK = True

except ImportError as e:
    pass


CLS_NAME_BY_ATTR_NAME = {
    "elastigroup.scheduling.tasks": "SchedulingTask",
    "elastigroup.scaling.up": "ScalingPolicy",
    "elastigroup.scaling.down": "ScalingPolicy",
    "elastigroup.strategy.signals": "Signal",
    "elastigroup.compute.launch_specification.managed_service_identities": "ManagedServiceIdentity",
    "elastigroup.compute.launch_specification.load_balancers_config": "LoadBalancerConfig",
    "elastigroup.compute.launch_specification.network.network_interfaces": "NetworkInterface",
    "elastigroup.compute.launch_specification.data_disks": "DataDisk",
    "elastigroup.compute.launch_specification.tags": "Tag",
    "elastigroup.compute.launch_specification.extensions": "Extension",
    "elastigroup.compute.launch_specification.secrets": "Secret",
}

LIST_MEMBER_CLS_NAME_BY_ATTR_NAME = {
    "elastigroup.scaling.up.action": "ScalingPolicyAction",
    "elastigroup.scaling.down.action": "ScalingPolicyAction",
    "elastigroup.scaling.up.dimensions": "ScalingPolicyDimension",
    "elastigroup.scaling.down.dimensions": "ScalingPolicyDimension",
    "elastigroup.compute.launch_specification.load_balancers_config.load_balancers": "LoadBalancer",
    "elastigroup.compute.launch_specification.network.network_interfaces.application_security_groups": "ApplicationSecurityGroup",
    "elastigroup.compute.launch_specification.network.network_interfaces.additional_ip_configurations": "AdditionalIpConfiguration",
    "elastigroup.compute.launch_specification.secrets.vault_certificates": "VaultCertificate"
}


def to_snake_case(camel_str):
    import re
    ret_val = re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

    return ret_val


def to_pascal_case(snake_str):
    return "".join(word.title() for word in snake_str.split("_"))


def is_primitive(some_obj):
    return any(isinstance(some_obj, x) for x in [bool, float, int, str])


def find_in_overrides(curr_path):
    return CLS_NAME_BY_ATTR_NAME.get(curr_path, None) or LIST_MEMBER_CLS_NAME_BY_ATTR_NAME.get(curr_path, None)


def get_client(module):
    creds_file_loaded_vars = dict()

    credentials_path = module.custom_params.get("credentials_path")

    if credentials_path is not None:
        try:
            with open(credentials_path, "r") as creds:
                for line in creds:
                    eq_index = line.find(":")
                    var_name = line[:eq_index].strip()
                    string_value = line[eq_index + 1:].strip()
                    creds_file_loaded_vars[var_name] = string_value
        except IOError:
            pass
    # End of creds file retrieval

    token = module.custom_params.get("token")
    if not token:
        token = creds_file_loaded_vars.get("token")

    account = module.custom_params.get("account_id")

    if not account:
        account = creds_file_loaded_vars.get("account")

    if account is not None:
        session = spotinst.SpotinstSession(auth_token=token, account_id=account)
    else:
        session = spotinst.SpotinstSession(auth_token=token)

    client = session.client("elastigroup_azure_v3")

    return client


def turn_to_model(content, field_name: str, curr_path=None):
    if content is None:
        return None
    elif is_primitive(content):
        return content
    elif isinstance(content, list):
        new_l = []

        for item in content:
            value = turn_to_model(item, field_name, curr_path)
            new_l.append(value)

        return new_l

    elif isinstance(content, dict):
        if curr_path is not None:
            curr_path += "." + field_name
        else:
            curr_path = field_name

        override = find_in_overrides(curr_path)
        key_to_use = override if override else to_pascal_case(field_name)

        class_ = getattr(spotinst.models.elastigroup.azure_v3, key_to_use)
        instance = class_()

        for key, value in content.items():
            new_value = turn_to_model(value, key, curr_path)
            setattr(instance, key, new_value)

        return instance


def find_group_id_with_same_name(groups, name):
    ret_val = []
    for group in groups:
        if group["name"] == name:
            ret_val.append(group)

    return ret_val


def clean_do_not_update_fields(
        elastigroup_module_copy: dict, do_not_update_list: list
):
    ret_val = elastigroup_module_copy

    # avoid deleting parent dicts before children
    do_not_update_list = sorted(do_not_update_list, key=len, reverse=True)

    for dotted_path in do_not_update_list:
        curr_dict = elastigroup_module_copy
        path_as_list = dotted_path.split(".")
        last_part_of_path = path_as_list[-1]

        for path_part in path_as_list[:-1]:
            new_dict = curr_dict.get(path_part)
            curr_dict = new_dict

        if curr_dict.get(last_part_of_path) is not None:
            del curr_dict[last_part_of_path]

    return ret_val


def get_id_and_operation(client, state: str, module):
    operation, id = None, None
    uniqueness_by = module.custom_params.get("uniqueness_by")
    manually_provided_group_id = module.custom_params.get("id")
    group = module.custom_params.get("elastigroup")

    if state == "present":

        if uniqueness_by == "id":
            if manually_provided_group_id is None:
                operation = "create"
            else:
                id = manually_provided_group_id
                operation = "update"
        else:
            all_groups = client.get_elastigroups()
            name = group["name"]
            groups_with_name = find_group_id_with_same_name(all_groups, name)

            if len(groups_with_name) == 0:
                operation = "create"
            elif len(groups_with_name) == 1:
                id = groups_with_name[0]["id"]
                operation = "update"
            else:
                msg = f"Failed updating elastigroup - 'uniqueness_by' is set to 'name' but there's more than one group with the name '{name}'"
                module.fail_json(changed=False, msg=msg)

    elif state == "absent":
        operation = "delete"

        if uniqueness_by == "id":
            if manually_provided_group_id is not None:
                id = module.custom_params.get("id")
            else:
                msg = "Failed deleting elastigroup - 'uniqueness_by' is set to `id` but parameter 'id' was not provided"
                module.fail_json(changed=False, msg=msg)
        else:
            all_groups = client.get_elastigroups()
            name = group["name"]
            groups_with_name = find_group_id_with_same_name(all_groups, name)

            if len(groups_with_name) == 1:
                id = groups_with_name[0]["id"]
            if len(groups_with_name) > 1:
                msg = f"Failed deleting elastigroup - 'uniqueness_by' is set to 'name' but there's more than one elastigroup with the name '{name}'"
                module.fail_json(changed=False, msg=msg)
            if len(groups_with_name) == 0:
                msg = f"Failed deleting elastigroup - 'uniqueness_by' is set to 'name' but there is no elastigroup with the name '{name}'"
                module.fail_json(changed=False, msg=msg)

    else:
        msg = f"Spot Ansible Module error: got unknown state {state}"
        module.fail_json(changed=False, msg=msg)
    return operation, id


def handle_elastigroup(client, module):
    eg_models = spotinst.models.elastigroup.azure_v3
    elastigroup_module_copy = copy.deepcopy(module.custom_params.get("elastigroup"))
    state = module.custom_params.get("state")

    operation, id = get_id_and_operation(client, state, module)

    if operation == "create":
        has_changed, group_id, message = handle_create_elastigroup(client, elastigroup_module_copy)
    elif operation == "update":
        has_changed, group_id, message = handle_update_elastigroup(client, elastigroup_module_copy, id, module)
    elif operation == "delete":
        has_changed, group_id, message = handle_delete_elastigroup(client, id, eg_models, module)
    else:
        module.fail_json(changed=False, msg=f"Unknown operation {operation} - "
                                            f"this is probably a bug in the module's code: please report")
        return None, None, None  # for IDE - fail_json stops execution

    return group_id, message, has_changed


def handle_delete_elastigroup(client, id, eg_models, module):
    group_id = id
    delete_args = dict(group_id=group_id)

    try:
        client.delete_elastigroup(**delete_args)
        message = f"Elastigroup {group_id} deleted successfully"
        has_changed = True
    except SpotinstClientException as exc:
        if "RESOURCE_DOES_NOT_EXIST" in exc.message:
            message = f"Failed deleting elastigroup - Elastigroup with ID {group_id} doesn't exist"
            module.fail_json(changed=False, msg=message)
        else:
            message = f"Failed deleting elastigroup (ID: {group_id}), error: {exc.message}"
            module.fail_json(msg=message)
        has_changed = False

    return has_changed, group_id, message


def handle_update_elastigroup(client, elastigroup_module_copy, id, module):
    elastigroup_module_copy = clean_do_not_update_fields(
        elastigroup_module_copy,
        module.custom_params.get("do_not_update")
    )
    ami_sdk_object = turn_to_model(elastigroup_module_copy, "elastigroup")

    try:
        res: dict = client.update_elastigroup(group_id=id, group_update=ami_sdk_object)
        group_id = res["id"]
        message = "Elastigroup updated successfully"
        has_changed = True

    except SpotinstClientException as exc:
        if "RESOURCE_DOES_NOT_EXIST" in exc.message:
            message = f"Failed updating elastigroup - elastigroup with ID {group_id} doesn't exist"
            module.fail_json(changed=False, msg=message)
        else:
            message = f"Failed updating elastigroup (ID {group_id}), error: {exc.message}"
            module.fail_json(msg=message)
        has_changed = False

    return has_changed, group_id, message


def handle_create_elastigroup(client, elastigroup_module_copy):
    ami_sdk_object = turn_to_model(
        elastigroup_module_copy, "elastigroup"
    )
   
    res: dict = client.create_elastigroup(group=ami_sdk_object)

    f = open("debug.txt", "w")
    f.write(json.dumps(res))
    f.close()

    group_id = res["id"]
    message = "Elastigroup created successfully"
    has_changed = True
    return has_changed, group_id, message


def main():
    global HAS_ANSIBLE_MODULE

    capacity_fields = dict(
        maximum=dict(type="int"),
        minimum=dict(type="int"),
        target=dict(type="int"),
    )

    health_fields = dict(
        health_check_types=dict(type="str"),
        auto_healing=dict(type="bool"),
        grace_period=dict(type="int"),
        unhealthy_duration=dict(type="int"),
    )

    task_fields = dict(
        is_enabled=dict(type="bool"),
        frequency=dict(type="str"),        
        start_time=dict(type="str"),
        cron_expression=dict(type="str"),
        type=dict(type="str"),
        scale_target_capacity=dict(type="int"),
        scale_min_capacity=dict(type="int"),
        scale_max_capacity=dict(type="int"),
        batch_size_percentage=dict(type="int"),
        grace_period=dict(type="int"),
        adjustment=dict(type="int"),
        adjustment_percentage=dict(type="int"),
        target_capacity=dict(type="int"),
        min_capacity=dict(type="int"),
        max_capacity=dict(type="int"),
    )

    scheduling_fields = dict(
        tasks=dict(type="list", elements="dict", options=task_fields)
    )

    scaling_policy_dimension_fields = dict(
        key=dict(type="str"),
        value=dict(type="str"),
    )

    scaling_policy_action_fields = dict(
        adjustment=dict(type="str"),
        type=dict(type="str"),
        minimum=dict(type="int"),
        maximum=dict(type="int"),
        target=dict(type="int"),               
    )

    scaling_policy_fields = dict(
        is_enabled=dict(type="bool"),
        policy_name=dict(type="str"),
        namespace=dict(type="str"),
        metric_name=dict(type="str"),
        dimensions=dict(type="list", elements="dict", options=scaling_policy_dimension_fields),
        statistic=dict(type="str"),
        unit=dict(type="str"),
        threshold=dict(type="float"),
        period=dict(type="int"),
        evaluation_periods=dict(type="int"),
        cooldown=dict(type="int"),
        action=dict(elements="dict", options=scaling_policy_action_fields),
        operator=dict(type="str"),
    )

    scaling_fields = dict(
        up=dict(type="list", elements="dict", options=scaling_policy_fields),
        down=dict(type="list", elements="dict", options=scaling_policy_fields),
    )

    revert_to_spot_fields = dict(perform_at=dict(type="str"))

    signal_fields = dict(
        type=dict(type="str"),
        timeout=dict(type="int"),
    )

    strategy_fields = dict(
        draining_timeout=dict(type="int"),
        fallback_to_od=dict(type="bool"),
        on_demand_count=dict(type="int"),
        optimization_windows=dict(type="list", elements="str"),
        orientation=dict(type="str"),
        revert_to_spot=dict(type="dict", options=revert_to_spot_fields),
        signals=dict(type="list", elements="dict", options=signal_fields),
        spot_percentage=dict(type="int"),

    )

    boot_diagnostics_fields = dict(
        is_enabled=dict(type="bool"),
        storage_uri=dict(type="str"),
        type=dict(type="str"),
    )

    data_disk_fields = dict(
        lun=dict(type="int"),
        size_g_b=dict(type="int"),
        type=dict(type="str"),
    )

    extension_fields = dict(
        api_version=dict(type="str"),
        auto_upgrade_minor_version=dict(type="bool"),
        minor_version_auto_upgrade=dict(type="bool"),
        name=dict(type="str"),
        publisher=dict(type="str"),
        type=dict(type="str"),
    )

    marketplace_image_fields = dict(
        publisher=dict(type="str"),
        offer=dict(type="str"),
        sku=dict(type="str"),
        version=dict(type="str"),
    )

    gallery_image_fields = dict(
        gallery_name=dict(type="str"),
        image_name=dict(type="str"),
        resource_group_name=dict(type="str"),
        spot_account_id=dict(type="str"),
        version=dict(type="str"),
    )

    custom_image_fields = dict(
        resource_group_name=dict(type="str"),
        name=dict(type="str"),
    )

    image_fields = dict(
        marketplace=dict(type="dict", options=marketplace_image_fields),
        custom=dict(type="dict", options=custom_image_fields),
        gallery=dict(type="dict", options=gallery_image_fields),
    )

    load_balancers_fields = dict(
        application_gateway_name=dict(type="str"),
        backend_pool_name=dict(type="str"),
        resource_group_name=dict(type="str"),
        type=dict(type="str"),
        auto_weight=dict(type="str"),
        balancer_id=dict(type="str"),
        target_set_id=dict(type="str"),
    )

    load_balancers_config_fields = dict(
        load_balancers=dict(type="list", elements="dict", options=load_balancers_fields)
    )

    login_fields = dict(
        ssh_public_key=dict(type="str"),
        user_name=dict(type="str"),
        password=dict(type="str"),
    )

    managed_service_identity_fields = dict(
        resource_group_name=dict(type="str"),
        name=dict(type="str"),
    )

    additional_ip_configuration_fields = dict(
        name=dict(type="str"),
        private_ip_address_version=dict(type="str"),
    )

    security_group_fields = dict(
        name=dict(type="str"),
        resource_group_name=dict(type="str"),
    )

    public_ip_fields = dict(
        name=dict(type="str"),
        resource_group_name=dict(type="str"),
    )

    network_interface_fields = dict(
        additional_ip_configurations=dict(type="list", elements="dict", options=additional_ip_configuration_fields),
        application_security_groups=dict(type="list", elements="dict", options=security_group_fields),
        assign_public_ip=dict(type="bool"),
        enable_ip_forwarding=dict(type="bool"),
        is_primary=dict(type="bool"),        
        private_ip_addresses=dict(type="list", elements="str"),
        public_ips=dict(type="list", elements="dict", options=public_ip_fields),
        public_ip_sku=dict(type="str"),
        security_group=dict(type="dict", options=security_group_fields),
        subnet_name=dict(type="str"),
    )

    network_fields = dict(
        network_interfaces=dict(type="list", elements="dict", options=network_interface_fields),
        virtual_network_name=dict(type="str"),
        resource_group_name=dict(type="str"),
    )

    os_disk_fields = dict(
        size=dict(type="str"),
        type=dict(type="str"),
    )

    source_vault_fields = dict(
        name=dict(type="str"),
        resource_group_name=dict(type="str"),
    )

    vault_certificate_fields = dict(
        certificate_store=dict(type="str"),
        certificate_url=dict(type="str"),
    )

    secret_fields = dict(
        source_vault=dict(type="dict", options=source_vault_fields),
        certificate_url=dict(type="list", elements="dict", options=vault_certificate_fields),
    )

    tags_fields = dict(tag_key=dict(type="str"), tag_value=dict(type="str"))

    launch_spec_fields = dict(
        boot_diagnostics=dict(type="dict", options=boot_diagnostics_fields),
        custom_data=dict(type="str"),
        data_disks=dict(type="list", elements="dict", options=data_disk_fields),
        extensions=dict(type="list", elements="dict", options=extension_fields),
        image=dict(type="dict", options=image_fields),
        load_balancers_config=dict(type="dict", options=load_balancers_config_fields),
        login=dict(type="dict", options=login_fields),
        managed_service_identities=dict(type="list", elements="dict", options=managed_service_identity_fields),
        network=dict(type="dict", options=network_fields),
        os_disk=dict(type="dict", options=os_disk_fields),
        secrets=dict(type="list", elements="dict", options=secret_fields),
        shutdown_script=dict(type="str"),
        tags=dict(type="list", elements="dict", options=tags_fields),
        vm_name_prefix=dict(type="str"),
    )

    vm_sizes_fields = dict(
        od_sizes=dict(type="list", elements="str"),
        preferred_spot_sizes=dict(type="list", elements="str"),
        spot_sizes=dict(type="list", elements="str"),
    )

    compute_fields = dict(
        launch_specification=dict(type="dict", options=launch_spec_fields),
        os=dict(type="str"),
        preferred_zones=dict(type="list", elements="str"),
        vm_sizes=dict(type="dict", options=vm_sizes_fields),
        zones=dict(type="list", elements="str"),
    )

    actual_fields = dict(
        name=dict(type="str", required=True),
        region=dict(type="str", required=True),
        resource_group_name=dict(type="str", required=True),
        description=dict(type="str"),
        scaling=dict(type="dict", options=scaling_fields),
        health=dict(type="dict", options=health_fields),
        scheduling=dict(type="dict", options=scheduling_fields),
        strategy=dict(type="dict", options=strategy_fields),
        compute=dict(type="dict", options=compute_fields),
        capacity=dict(type="dict", options=capacity_fields),
    )

    fields = dict(
        # region config fields
        token=dict(
            type="str", fallback=(env_fallback, ["SPOTINST_TOKEN"]), no_log=True
        ),
        credentials_path=dict(type="path", default="~/.spotinst/credentials"),
        state=dict(type="str", default="present", choices=["present", "absent"]),
        account_id=dict(
            type="str", fallback=(env_fallback, ["SPOTINST_ACCOUNT_ID", "ACCOUNT"])
        ),
        id=dict(type="str"),
        uniqueness_by=dict(type="str", choices=["id", "name"], default="name"),
        do_not_update=dict(type="list", elements="str"),
        # endregion

        # region elastigroup
        elastigroup=dict(type="dict", required=True, options=actual_fields)
        # endregion
    )

    # unchecked imports are not allowed for modules
    # so we have to guard against the import AnsibleModule statement, even though AnsibleModule
    # is part of ansible-core.
    try:
        module = SpotAnsibleModule(argument_spec=fields)
    except (AttributeError, NameError, ImportError):
        module = AnsibleModule(argument_spec=fields)
        HAS_ANSIBLE_MODULE = False

    if not HAS_ANSIBLE_MODULE:
        module.fail_json(
            msg="the Spotinst Ansible module is required."
        )

    if not HAS_SPOTINST_SDK:
        module.fail_json(
            msg="the Spotinst SDK library is required. (pip install spotinst-sdk2)"
        )

    client = get_client(module=module)

    group_id, message, has_changed = handle_elastigroup(
        client=client, module=module
    )

    module.exit_json(
        changed=has_changed, group_id=group_id, message=message
    )


if __name__ == "__main__":
    main()
