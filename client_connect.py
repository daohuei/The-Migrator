import requests
import socket
import json
from datetime import datetime
import time
# send message
def send_message_udp(u_socket ,u_IP, u_PORT, u_Message):
	print("UDP target IP:" + u_IP) 
	print("UDP target port:" + str(u_PORT)) 
	#tic = time.perf_counter()
	timestamp_msg = str(datetime.timestamp(datetime.now()))
	msg = timestamp_msg
	u_socket.sendto(msg.encode(), (u_IP, u_PORT))
	#toc = time.perf_counter()
	#tictoc = toc - tic
	#print(format(tictoc, ".9f") + " seconds")

def connect_server():
	url = 'http://128.110.155.6:5001'
	hostname = socket.gethostname()
	client_info = {'name': hostname}
	connect_request = requests.post(url+'/client_connect', json = client_info)

	return json.loads(connect_request.text)

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
	print(type(connect_info))
	print(connect_info)
	# UDP
	while True:
		time.sleep(2)
		UDP_IP_LIST = connect_info['node_list']
		for UDP_IP in UDP_IP_LIST:
			send_message_udp(sock, UDP_IP, UDP_PORT, MESSAGE)

if __name__ == "__main__":
	main()