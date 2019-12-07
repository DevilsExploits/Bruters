import threading
import requests
import socket
import json
import sys

def scan(dir):
    try:
        r = requests.get("http://"+target+"/"+dir.strip())
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((target, 80))
        ipaddress = s.getpeername()[0]
        if r.status_code == 403 or r.status_code == 200:
            print("https://{}/{} Found [{}]".format(target,dir.strip(), r.status_code))
    except socket.error:
        pass

if len(sys.argv) < 3:
    print("{} [TARGET] [LIST]".format(sys.argv[0]))
    exit()
else:
    target = sys.argv[1]
    dirlist = open(sys.argv[2], "r").readlines()

for i in range(0,100):
    for dir in dirlist:
        i += 1

        thread = threading.Thread(target=scan, args=(dir.strip(),))
        thread.start()
        
        if i == 100:
            thread.join()
            i = 0