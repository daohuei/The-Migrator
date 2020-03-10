import requests
import psutil
import platform
from datetime import datetime
import socket

localhost = "0.0.0.0"
UDP_PORT = 5002

def get_size(bytes, suffix="B"):
	"""
	Scale bytes to its proper format
	e.g:
		1253656 => '1.20MB'
		1253656678 => '1.17GB'
	"""
	factor = 1024
	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < factor:
			return f"{bytes:.2f}{unit}{suffix}"
		bytes /= factor

def get_os_info():
	os_info = dict()
	os_info["cpu"] = psutil.cpu_percent() # cpu percentage
	os_info["memory"] = get_size(psutil.virtual_memory().available) # memory percentage
	os_info["disk_usage"] = get_size(psutil.disk_usage(psutil.disk_partitions()[0].mountpoint).free) # size of free space(in GB)
	os_info["hostname"] = socket.gethostname()
	return os_info

def main():
	ctl_url = 'http://128.110.155.6:5001'
	ctl_url_page = '/update_node' 
	#register_request = requests.post(ctl_url+ctl_url_page, data = register_stat)
	sock = socket.socket(socket.AF_INET, # Internet
						socket.SOCK_DGRAM) # UDP
	sock.bind((localhost, UDP_PORT))
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		client_timestamp = float(str(data, 'utf-8'))
		server_timestamp = datetime.timestamp(datetime.now())
		message = get_os_info()
		latency_timestamp = server_timestamp - client_timestamp
		latency = latency_timestamp
		message['latency'] = latency
		print(message)
		print(latency_timestamp)
		update_request = requests.post(ctl_url+ctl_url_page, json = message)
		print(update_request.text)

if __name__ == "__main__":
	main()
"""
ctl_url = 'http://128.110.155.6:5001'
register_stat = {'client': 'tingken0214','password':'hi'}

x = requests.post(ctl_url+'/client_connect', data = myobj)
print(x.text)
myobj3 = {'client': "chuchu",'password':'bgdsf'}

x3 = requests.post(url+'/client_connect', data = myobj3)
print(x3.text)
"""