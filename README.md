# Spot Cloud Modules Collection

The Spot Cloud Modules Ansible collection includes Ansible modules to help automate the management of Spot resources.

**Note:** If you are migrating to this collection from the module in `community.general` or the previous Github repo, please read [the migration guide](#migrating-from-spots-previous-modules) below.  

<!--start requires_ansible-->
## Ansible version compatibility
This collection has been tested against following Ansible versions: **>=2.9.10**.
<!--end requires_ansible-->

## Python version compatibility

Version 2 of Spot's Python SDK does not support Python 2.7 so this collection requires Python 3.6 or greater.

## Spot Python SDK compatibility

Version `1.2.0` of this collection requires at least version `2.1.30` of Spot's Python SDK.

## Included content

<!--start collection content-->
### Modules

Name | Description
--- | ---
[spot.cloud_modules.aws_elastigroup](https://github.com/spotinst/spot-ansible-cloud-modules/blob/main/docs/examples/elastigroup/README.md)|Manage Spot Elastigroups
[spot.cloud_modules.aws_managed_instance](https://github.com/spotinst/spot-ansible-cloud-modules/blob/main/docs/examples/managed_instance/README.md)|Manage Spot Managed Instances
[spot.cloud_modules.aws_ocean_k8s](https://github.com/spotinst/spot-ansible-cloud-modules/blob/main/docs/examples/ocean/README.md)|Manage Spot Ocean Kubernetes Clusters
[spot.cloud_modules.aws_mrscaler](https://github.com/spotinst/spot-ansible-cloud-modules/blob/main/docs/examples/emr/README.md)|Manage Spot MR Scalers
[spot.cloud_modules.event_subscription](https://github.com/spotinst/spot-ansible-cloud-modules/blob/main/docs/examples/events/README.md)|Manage Spot Event Subscriptions
[spot.cloud_modules.azure_stateful_node](https://github.com/spotinst/spot-ansible-cloud-modules/blob/main/docs/examples/stateful_node/README.md)|Manage Azure Stateful Nodes
[spot.cloud_modules.azure_elastigroup](https://github.com/spotinst/spot-ansible-cloud-modules/blob/main/docs/examples/elastigroup/README.md)|Manage Azure Elastigroups
<!--end collection content-->

## Installing this collection

You can install the Spot collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install spot.cloud_modules

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: spot.cloud_modules
```

The python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip and from the collection project's root, running:

    pip install requirements.txt
or:

    pip install spotinst_sdk2>=2.1.30

## Using this collection

You can either call modules by their Fully Qualified Collection Namespace (`FQCN`), such as `spot.cloud_modules.aws_elastigroup`, or you can call modules by their short name if you list the `spot.cloud_modules` collection in the playbook's `collections` keyword:

```yaml
---
# FQCN 
  tasks:
    - name: Manage Elastigroup
      spot.cloud_modules.aws_elastigroup:
```

```yaml
---
# collections keyword
 collections:
    - spot.cloud_modules
  
  tasks:
    - name: Manage Elastigroup
      aws_elastigroup:
```

## Migrating from Spot's previous modules

*This section does **not** apply to you if you are upgrading from a previous version of **this** collection.*

If you are migrating either from `community.general` or from previously having our `spotinst_aws_elastigroup` installed manually, please take note of the following breaking changes:

### Migrating from `community.general`

- Python `>=3.6` required.
- `spotinst_sdk2` (v2) required (`community.general.spotinst_aws_elastigroup` required `spotinst_sdk` (v1)).
- The module `community.general.spotinst_aws_elastigroup` was renamed to `spot.cloud_modules.aws_elastigroup` in this collection.

### Migrating from manual installation

- Python `>=3.6` required.
- `spotinst_sdk2` (v2) required (your version may have required `spotinst_sdk` (v1)).
- All references to modules should be changed to `spot.cloud_modules.module_name`, according to the module names in [the modules section](#modules).
  - Note: all modules have been renamed.

## Contributing

Contributions to this collection are welcome.

## Code of conduct

Please be sure to read our [Code of Conduct](CODE_OF_CONDUCT.md).
