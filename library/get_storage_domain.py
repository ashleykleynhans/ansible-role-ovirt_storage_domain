#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ansible.module_utils.basic import AnsibleModule
from distutils.version import LooseVersion
import json


try:
  import ovirtsdk4 as sdk

  OVIRTSDK_FOUND = True
except ImportError:
   OVIRTSDK_FOUND = False


def get_storage_domain(connection, cluster, blacklisted_domains):
  storage_domain = None

  # Create the Clusters Service
  clusters_service = connection.system_service().clusters_service()

  # Get the list of Storage Domains for the service that Match the Cluser Name
  clstr = clusters_service.list(search='name={cluster}'.format(cluster=cluster), max=1, follow='data_center.storage_domains')
  clstr = clstr[0]

  for sd in clstr.data_center.storage_domains:
    if storage_domain is None and sd.name not in blacklisted_domains:
      storage_domain = sd
      continue

    if sd.available is not None and sd.name not in blacklisted_domains and sd.available > storage_domain.available:
      storage_domain = sd

  # Close the connection to the server:
  connection.close()

  return storage_domain.name


def main():
  argument_spec = dict(
   engine_url          = dict(type="str", required=True),
   engine_user         = dict(type="str", required=True),
   engine_password     = dict(type="str", required=True, no_log=True),
   engine_cafile       = dict(type="str", required=True, no_log=True),
   cluster             = dict(type="str", required=True),
   blacklisted_domains = dict(type="list", required=False), 
  )

  a_module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

  if not OVIRTSDK_FOUND:
    a_module.fail_json(msg="ovirtsdk4 library is required for this module")

  # FIXME: Version check is not working
  #if sdk.__version__ and LooseVersion(sdk.__version__) < LooseVersion("4.3.3"):
  #    a_module.fail_json(msg="ovirtsdk4 library version should be >= 4.3.3")

  if a_module.params["engine_url"] and a_module.params["engine_url"] == 'https://host.example.com/ovirt-engine/api':
    a_module.fail_json(msg="engine_url variable has not been changed from default")

  if a_module.params["engine_password"] and a_module.params["engine_password"] == 'password':
    a_module.fail_json(msg="engine_password variable has not been changed from default")

  if not a_module.params["engine_cafile"]:
    a_module.fail_json(msg="engine_cafile variable has not been provided")

  if a_module.params["cluster"] and a_module.params["cluster"] == 'example_cluster':
    a_module.fail_json(msg="cluster variable has not been changed from default")

  if a_module.params["blacklisted_domains"]:
    blacklisted_domains = a_module.params["blacklisted_domains"]
  else:
    blacklisted_domains = []

  result = dict(changed=False)

  # Create the connection to the server:
  connection = sdk.Connection(
    url      = a_module.params["engine_url"],
    username = a_module.params["engine_user"],
    password = a_module.params["engine_password"],
    ca_file  = a_module.params["engine_cafile"]
  )

  # Get the storage domains that match example_dc and return the one with
  # the most available disk space
  sd = get_storage_domain(connection, a_module.params["cluster"], a_module.params["blackisted_domains"])

  if sd is not None:
    result["changed"] = True
    result["storage_domain"] = sd

  a_module.exit_json(**result)


if __name__ == "__main__":
  main()
