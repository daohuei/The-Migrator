import requests
import socket
import json
from datetime import datetime
import time
import threading
import os
# send message
def send_message_udp(u_socket ,u_IP, u_PORT, u_Message):
	#print("UDP target IP:" + u_IP) 
	#print("UDP target port:" + str(u_PORT)) 
	#tic = time.perf_counter()
	timestamp_msg = str(datetime.timestamp(datetime.now()))
	msg = u_Message + "," + timestamp_msg
	u_socket.sendto(msg.encode(), (u_IP, u_PORT))
	#toc = time.perf_counter()
	#tictoc = toc - tic
	#print(format(tictoc, ".9f") + " seconds")

def connect_server():
	url = 'http://128.110.155.6:5001'
	hostname = socket.gethostname()
	client_info = {'name': hostname}
	connect_request = requests.post(url+'/client_connect', json = client_info)
	connect_info_dict = {}
	try:
		connect_info_dict = json.loads(connect_request.text)
	except Exception as e:
		print(str(e))
	return connect_info_dict

def udp_thread():
	UDP_IP_LIST = [
	"128.110.155.27",
	"128.110.154.244",
	"128.110.155.8",
	"128.110.155.20"]
	UDP_PORT = 5002
	msg_len = 1000
	MESSAGE = "a" * msg_len
	sock = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP
	connect_info = dict()
	try:
		with open('connect_info.json', 'r') as rfile:
			data_text = json.load(rfile)
			connect_info = json.loads(data_text)			
			#print(type(data_text))
			#print(type(connect_info))
		# UDP
		while True:
			time.sleep(15)
			UDP_IP_LIST = connect_info['node_list']
			for UDP_IP in UDP_IP_LIST:
				send_message_udp(sock, UDP_IP, UDP_PORT, MESSAGE)
	except Exception as e:
		print(str(e))

def test_program(v_ip):
	"""
	while True:
		time.sleep(1)
		os.system("cat test_program.py | ssh "+ 
				socket.gethostname() +"@"+
				v_ip+" python -")
	"""
	ret = 0
	while ret == 0:
		ret = os.system("ping v_ip")

def ping_test(v_ip):	
	ret = 0
	while ret == 0:
		time.sleep(1)
		ret = os.system("ping -w 5 "+v_ip)
		print(ret)
	print("disconnection")

# "128.110.155.6": ctl
# "128.110.155.27": cp-1
# "128.110.154.244": cp-2
# "128.110.155.8": cp-3
# "128.110.155.20": cp-4

def main():
	UDP_IP_LIST = [
	"128.110.155.27",
	"128.110.154.244",
	"128.110.155.8",
	"128.110.155.20"]
	UDP_PORT = 5002
	MESSAGE = ""
	connect_info = connect_server()
	sock = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP
	info_json = json.dumps(connect_info, sort_keys=True, indent=4)
	if 'status' in connect_info.keys() and connect_info['status'] == "Succeed":
		with open('connect_info.json', 'w') as outfile:
			json.dump(info_json, outfile)
		print(connect_info)
		#os.system('python3 udp_client.py')
		udp_client_thread = threading.Thread(target=udp_thread)
		udp_client_thread.start()
		print ('connection established\n')
		#test_program(connect_info['address'])
		time.sleep(10)
		ping_test(connect_info['address'])
	else:
		print('connection failed\n')
		print(connect_info)

if __name__ == "__main__":
	main()