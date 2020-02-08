ovirt storage domain
====================

Ansible role to get a list of oVirt storage domains through the oVirt REST API, and return the name of the storage domain with the most available storage capacity.

Requirements
------------

* ovirt-engine-sdk-python
* pycurl

Role Variables
--------------

ovirt_hostname: "host.example.com"
ovirt_username: "admin@internal"
ovirt_password: "password"
ovirt_data_centre: "example_dc"

For security reasons, it is strongly recommended to use Ansible vault to encrypt the *ovirt_password*.

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
