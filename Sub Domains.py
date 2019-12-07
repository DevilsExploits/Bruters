import sys
import json
import socket
import requests
import threading

if len(sys.argv) < 3:
	sys.exit("Usage: {} <Target> <Threads> <List>".format(sys.argv[0]))

target = sys.argv[1]
threads = int(sys.argv[2])

i = 0

def get_route(ip):
	r = requests.get("http://r.0xy.me/" + ip + "/route")

	return r.text

def get_hostname(ip):
	r = requests.get("http://r.0xy.me/" + ip + "/hostname")
	result = json.loads(r.text)

	return result["hostname"]

def scan(sub):
	try:
		r = requests.get("http://" + sub + "." + target)

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(10)

		sock.connect((sub + "." + target, 80))
		
		ipaddress = sock.getpeername()[0]
		hostname = get_hostname(ipaddress)
		route = get_route(ipaddress)

		if hostname and r.status_code not in (404, 405):
			print("{} Connected [RESOLVED: {}] [ROUTE: {}] [HOSTNAME: {}]".format(sub, ipaddress,route, hostname))
	except socket.error:
		pass

with open(sys.argv[3], "r") as fd:
	lines = fd.readlines()

for sub in lines:
	i += 1

	thread = threading.Thread(target=scan, args=(sub.strip(),))
	thread.start()
	
	if i == threads:
		thread.join()
		i = 0
