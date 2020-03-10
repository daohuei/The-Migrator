#!/usr/bin/python3
import os
import time
from .controller import Controller
from neutronclient.v2_0 import client as ncli
from novaclient import client, v2, exceptions
from keystoneauth1.identity import v3
from keystoneauth1 import session

USERNAME = 'adminapi'
PASSWORD = os.getenv('OS_PASSWORD')
AUTH_URL = os.getenv('OS_AUTH_URL')
PROJECT_NAME = 'admin'
DOMAIN_NAME = 'default'
VERSION = 2.13

class OpenStackController(Controller):
    def __init__(self):
        auth = v3.Password(auth_url=AUTH_URL,
                        username=USERNAME,
                        password=PASSWORD,
                        project_name=PROJECT_NAME,
                        project_id='0ca4618de5bc4f7da7587356ce1431e5',
                        project_domain_name=DOMAIN_NAME,
                        user_domain_name=DOMAIN_NAME)

        sess = session.Session(auth=auth)
        self.neutron = ncli.Client(session=sess)
        self.nova = client.Client(VERSION, session=sess)
        self.clientlist = dict()

    def get_host_from_ip(self, ip):

        info = v2.hypervisors.HypervisorManager(self.nova).get(host)
        d = {'host_ip': info.host_ip, 'free_ram_mb':info.free_ram_mb, \
                'free_disk_gb': info.free_disk_gb, 'current_wordload': info.current_workload}

    def get_host_list(self):
        ret = list()
        for host in self.nova.hypervisors.list():
            info = v2.hypervisors.HypervisorManager(self.nova).get(host)
            d = {'host_ip': info.host_ip, 'free_ram_mb':info.free_ram_mb, \
                    'free_disk_gb': info.free_disk_gb, 'current_wordload': info.current_workload}
            ret.append(d)

        return ret

    def get_server_list(self):
        return self.client.servers.list()

    def map_to_instance(self, name):
        try:
            # Create instance
            image = v2.images.GlanceManager(self.nova).find_image('xenial-server')
            flavor = v2.flavors.FlavorManager(self.nova).get(2) #m1-small
            nic = [{'tag': '','net-id':'79922196-41b3-42d7-8b9c-a2f4bb25395b'}]
            server = v2.servers.ServerManager(self.nova).create(name, image, flavor, nics=nic)

            # Assign floating IP
            time.sleep(5) # It takes some time to allocate a network interface automatically
            print(server.interface_list()[0].id)
            for x in self.neutron.list_floatingips()['floatingips']:
                if x['status'] != 'ACTIVE':
                    self.neutron.update_floatingip(x['id'], {'floatingip':{'port_id':server.interface_list()[0].id}}) 
                    return ('Succeed', x['floating_ip_address'])

            return ('Failed', 'VM creation failed')
        except exceptions.NotFound:
            return ('Failed', 'VM creation failed')
        
    def migrate(self, instance, target):
        pass
