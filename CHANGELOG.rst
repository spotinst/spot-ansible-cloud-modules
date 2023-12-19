================================
Spot Cloud Modules Release Notes
================================

.. contents:: Topics


v1.0.0
======

Release Summary
---------------

New collection - adding all existing modules.

New Modules
-----------

- spot.cloud_modules.aws_elastigroup - Manage (Create, Update, Delete) Spot AWS Elastigroups
- spot.cloud_modules.aws_managed_instance - Create, update or delete Spot AWS Managed Instances
- spot.cloud_modules.aws_mrscaler - Create, update or delete Spot MRScaler
- spot.cloud_modules.aws_ocean_k8s - Create, update or delete Spot Ocean K8s
- spot.cloud_modules.event_subscription - Create event subscription for resource


v1.1.0
======

Release Summary
---------------

Adding support for Azure Stateful Nodes.

New Modules
-----------

- spot.cloud_modules.azure_stateful_node - Manage (Create, Update, Delete) Azure Stateful Nodes


v1.2.0
======

Release Summary
---------------

Adding support for Azure Elastigroups.

New Modules
-----------

- spot.cloud_modules.azure_elastigroup - Manage (Create, Update, Delete) Azure Elastigroups


v1.3.0
======

Release Summary
---------------

Adding support to create Azure Stateful Node by Importing an Azure VM.


v1.3.1
======

Release Summary
---------------

Made delete operation idempotent for azure_stateful_node

Bugfixes
--------

- spot.cloud_modules.azure_stateful_node - When 'delete by name' operation is triggered for a non-existent node, return success, not exception.


v1.3.2
======

Release Summary
---------------

Added new fields in azure_stateful_node module.


v1.3.3
======

Release Summary
---------------

- spot.cloud_modules.azure_stateful_node - Added `public_settings` and `protected_settings` fields in the `extensions` object.