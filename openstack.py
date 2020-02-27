#!/usr/bin/python3
import os
from novaclient import client, v2
from keystoneauth1 import loading
from keystoneauth1 import session

USERNAME = 'adminapi'
PASSWORD = os.getenv('OS_PASSWORD')
AUTH_URL = os.getenv('OS_AUTH_URL')
PROJECT_NAME = 'admin'
DOMAIN_NAME = 'default'
VERSION = 2.13

class OpenStackController():
    def __init__():
        self.client = client.Client(VERSION, auth_url=AUTH_URL,
                                username=USERNAME,
                                password=PASSWORD,
                                project_name=PROJECT_NAME,
                                project_domain_name=DOMAIN_NAME,
                                user_domain_name=DOMAIN_NAME)

    def get_host_list():
        for host in self.client.hypervisors.list():
            info = v2.hypervisors.HypervisorManager(nova).get(host)
            print(info.cpu_info)

    def get_server_list():
        return self.client.servers.list()

    def migrate(instance, target):
        pass
