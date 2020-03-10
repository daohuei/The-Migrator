import requests
import psutil
import platform
from datetime import datetime
import socket
import uuid
import socket
import time
import _thread
from datetime import datetime

def get_public_ip():
    # my_uuid = uuid.uuid1()
    hostname = socket.gethostname()    
    # print(uuid.uuid3(uuid.NAMESPACE_DNS, hostname))
    # print(uuid.uuid5(uuid.NAMESPACE_DNS, hostname))
    IPAddr = socket.gethostbyname(hostname) 
    return {'hostname':hostname, 'public_ip':IPAddr}

def main():
    ctl_url = 'http://128.110.155.6:5001'
    ctl_url_page = '/register' 
    register_stat = get_public_ip()
    register_request = requests.post(ctl_url+ctl_url_page, json = register_stat)

if __name__ == "__main__":
    main()