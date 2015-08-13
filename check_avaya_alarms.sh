#!/bin/bash

# Quick script to login to the Avaya servers using command sshpass
# sshpass allows us to specify a password on the command line.
#
# This will log into the PBX, grab alarms and return it to a variable
# all in 1 command. We will trigger off the "EvtID" column since
# this only exists while there are alarms present, and it is unique
# enough to reduce false positives.
#
# Pat O'Brien - June 17, 2014

# User input: hostname username password
# Example: check_avaya_alarms_new.sh avaya_hostname username password

# Bash exit codes for Nagios:
# 0 = OK
# 1 = WARNING
# 2 = CRITICAL
# 3 = UNKNOWN

HOST=$1
USER=$2
PASSWORD=$3

VAR=$(/usr/bin/sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no $USER@$HOST /opt/ecs/bin/almdisplay)

if [[ -z $VAR ]]; then
	echo "Error: Alarms could not be found for this host. You could have a bad login."
	exit 2
fi

if [[ $VAR == *EvtID* ]]; then
	echo "CRITICAL: Avaya is reporting an alarm. Please investigate."
	exit 2
else
	echo "OK: Avaya reports no alarms."
	exit 0
fi
