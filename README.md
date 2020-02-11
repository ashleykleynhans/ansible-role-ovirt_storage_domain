ovirt storage domain
====================

Ansible role to get a list of oVirt storage domains through the oVirt REST API, and return the name of the storage domain with the most available storage capacity.

Requirements
------------

* ovirt-engine-sdk-python
* pycurl

Role Variables
--------------

    engine_url: "https://host.example.com/ovirt-engine/api"
    engine_user: "admin@internal"
    engine_password: "password"
    engine_cafile:  "CA_FILE_PATH"
    cluster: "example_cluster"

For security reasons, it is strongly recommended to use Ansible vault to encrypt the *engine_password*.

Dependencies
------------

None

Example Playbook
----------------

    - hosts: localhost
      roles:
         - ovirt_storage_domain

License
-------

Apache2

Author Information
------------------

Ashley Kleynhans
