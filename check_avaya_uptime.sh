#!/bin/bash
# Quick script to login to the Avaya servers using command sshpass
# sshpass allows us to specify a password on the command line
#
# This will log into the server, grab uptime and return it to a variable
# all in 1 command. 
#
# Avaya recommends rebooting CM every 6 months. This script helps us keep track of uptimes.
#
# Pat O'Brien - June 24, 2014

# User input: hostname username password uptime_threshold_in_days
# Example: check_avaya_uptime.sh avayaHostname username password 120 (this number is the alarm threshold)

# Bash exit codes for Nagios:
# 0 = OK
# 1 = WARNING
# 2 = CRITICAL
# 3 = UNKNOWN

HOST=$1
USER=$2
PASSWORD=$3
THRESHOLD=$4

uptime=$(/usr/bin/sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no $USER@$HOST "cat /proc/uptime")
uptime=${uptime%%.*}

days=$(( uptime/60/60/24 ))


if [[ -z $uptime ]]; then
	echo "Error: Uptime could not be found for this host. You could have a bad login."
	exit 2
fi

if [ $days -le $THRESHOLD ]; then
	echo "OK: Uptime is" $days "days, which is within the required threshold of" $THRESHOLD "days."
	exit 0		
else 
	echo "WARNING: Uptime is currently" $days "days and is OVER the threshold of" $THRESHOLD "days."
	exit 1
fi

