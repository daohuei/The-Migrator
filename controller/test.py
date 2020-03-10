#!/usr/bin/python3
import os
import time
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

auth = v3.Password(auth_url=AUTH_URL,
                username=USERNAME,
                password=PASSWORD,
                project_name=PROJECT_NAME,
                project_id='0ca4618de5bc4f7da7587356ce1431e5',
                project_domain_name=DOMAIN_NAME,
                user_domain_name=DOMAIN_NAME)

_client = client.Client(VERSION, auth_url=AUTH_URL,
                username=USERNAME,
                password=PASSWORD,
                project_name=PROJECT_NAME,
                project_domain_name=DOMAIN_NAME,
                user_domain_name=DOMAIN_NAME)

_nclient = ncli.Client(session=session.Session(auth=auth))
clientlist = dict()

def get_host_list(self):
    ret = list()
    for host in self.client.hypervisors.list():
        info = v2.hypervisors.HypervisorManager(self.client).get(host)
        d = {'host_ip': info.host_ip, 'free_ram_mb':info.free_ram_mb, \
                'free_disk_gb': info.free_disk_gb, 'current_wordload': info.current_workload}
        ret.append(d)

    return ret

def get_server_list():
    return _client.servers.list()

def map_to_instance(name):
    try:
        image = v2.images.GlanceManager(_client).find_image('xenial-server')
        print(image)
        flavor = v2.flavors.FlavorManager(_client).get(2) #m1-small
    except NotFound:
        return null
    nic = [{'tag': '','net-id':'79922196-41b3-42d7-8b9c-a2f4bb25395b'}]
    server = v2.servers.ServerManager(_client).create(name, image, flavor, nics=nic)
    #print(dir(v2.hypervisors.HypervisorManager(_client).get()))
    #time.sleep(5)
    print(server.interface_list()[0].id)

    for x in _nclient.list_floatingips()['floatingips']:
        if x['status'] != 'ACTIVE':
            print(server.hostId)
            #_nclient.update_floatingip(x['id'], {'floatingip':{'port_id':server.interface_list()[0].id}}) 
            print(x['id'])
            break
   
print(get_server_list())
map_to_instance('123')

