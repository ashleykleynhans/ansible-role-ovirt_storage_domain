#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ansible.module_utils.basic import AnsibleModule
from distutils.version import LooseVersion
import json
import re


try:
    import ovirtsdk4 as sdk

    OVIRTSDK_FOUND = True
except ImportError:
     OVIRTSDK_FOUND = False


def get_storage_domain(connection, dc):
    dc = dc.upper()
    storage_domain = None

    # Create the storage domain service and get a list of storage domains
    sds_service = connection.system_service().storage_domains_service()
    storage_domains = sds_service.list()

    # Iterate over the storage domains and get the used and available
    # disk space for each
    for sd in storage_domains:
        match = re.match("^\w+_(" + dc + ")_\w+$", sd.name)

        if not match:
            continue

        if storage_domain is None:
            storage_domain = sd
            continue

        if sd.available is not None and sd.available > storage_domain.available:
            storage_domain = sd

    # Close the connection to the server:
    connection.close()

    return storage_domain.name


def main():
    argument_spec = dict(
        ovirt_hostname=dict(type="str", required=True),
        ovirt_username=dict(type="str", required=True),
        ovirt_password=dict(type="str", required=True, no_log=True),
        ovirt_data_centre=dict(type="str", required=True)
    )

    a_module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if not OVIRTSDK_FOUND:
        a_module.fail_json(msg="ovirtsdk4 library is required for this module")

    # FIXME: Version check is not working
    #if sdk.__version__ and LooseVersion(sdk.__version__) < LooseVersion("4.3.3"):
    #    a_module.fail_json(msg="ovirtsdk4 library version should be >= 4.3.3")

    if a_module.params["ovirt_hostname"] and a_module.params["ovirt_hostname"] == 'host.example.com':
        a_module.fail_json(msg="ovirt_hostname variable has not been changed from default")

    if a_module.params["ovirt_username"] and a_module.params["ovirt_username"] == 'default@internal':
        a_module.fail_json(msg="ovirt_username variable has not been changed from default")

    if a_module.params["ovirt_password"] and a_module.params["ovirt_password"] == 'password':
        a_module.fail_json(msg="ovirt_password variable has not been changed from default")

    if a_module.params["ovirt_data_centre"] and a_module.params["ovirt_data_centre"] == 'example_dc':
        a_module.fail_json(msg="ovirt_data_centre variable has not been changed from default")

    result = dict(changed=False)

    # Create the connection to the server:
    connection = sdk.Connection(
        url="https://{fqdn}/ovirt-engine/api".format(fqdn=a_module.params["ovirt_hostname"]),
        username=a_module.params["ovirt_username"],
        password=a_module.params["ovirt_password"],
        insecure=True,
        debug=True
    )

    # Get the storage domains that match example_dc and return the one with
    # the most available disk space
    sd = get_storage_domain(connection, a_module.params["ovirt_data_centre"])

    if sd is not None:
        result["changed"] = True
        result["storage_domain"] = sd

    a_module.exit_json(**result)


if __name__ == "__main__":
    main()
