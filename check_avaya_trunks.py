#
# This script will login to the Avaya CM using telnet. It will check the trunks
# in the list, and look for any out of service conditions. 
#
# Example usage:
# sudo python check_avaya_trunks.py <hostname> <user> <password> <"trunk, group, list">
# sudo python check_avaya_trunks.py avayaHostname username password "1,2,5"
#
# Pat O'Brien, January 21, 2015

# Nagios Exit Codes
# 0: OK - sys.exit(0)
# 1: Warning - sys.exit(1)
# 2: Critical - sys.exit(2)
# 3: Unknown - sys.exit(3)

import os, sys
import telnetlib
from time import sleep

# Variables. Wrapped in brackets symbolizes a list
HOSTS = [sys.argv[1]]
USER = sys.argv[2]
PASS = sys.argv[3]
TRUNKS = [x.strip() for x in sys.argv[4].split(',')]
trunksBadList = []

# Verbiage to trigger off of
NOTRUNK = [ "Group not assigned" ]
OOS = [ "OOS/FE-idle", "out-of-service", "out-of-service-NE" ]

# Use the built in Python any() function. Break down the words in OUTPUT
# and compare them to the words in NOTRUNK or OOS. If there's a match,
# it'll return TRUE. 
def parseOutput(OUTPUT, trunk):
	if any( word in OUTPUT for word in NOTRUNK ):
		print "CRITICAL: Invalid trunk number " + trunk + ". Check the Nagios service config."
		sys.exit(3)
	elif any( word in OUTPUT for word in OOS ):
		# Found a trunk that has out of service members. Add it to the naughty list
		trunksBadList.append(trunk)
			
# Exit to Nagios with the list of trunks that are bad
def exitToNagios(trunksBad):
	if trunksBad:
		trunks = ", ".join(trunksBad)
		print "CRITICAL: Out Of Service condition found on trunk " + trunks
		sys.exit(2)
	else:
		allTrunks = ", ".join(TRUNKS)
		print "OK: All trunks in service. Trunks checked: " + allTrunks
		sys.exit(0)

# Parse the list of hosts and trunk groups. 
# The sleeps are to slow down telnetlib, and allow Avaya to respond.
for host in HOSTS:
	tn = telnetlib.Telnet(host)

	# Debugging
	#tn.set_debuglevel(5)

	# Login
	tn.read_until("login: ")
	tn.write(USER + "\n")
	tn.read_until("Password: ")
	tn.write(PASS + "\n")

	# Select shell terminal
	tn.read_until("Enter your terminal type (i.e., xterm, vt100, etc.) [vt100]=>")
	tn.write("vt100\n")
	sleep(0.5)

	# Setup the autosat
	tn.write("autosat\n")
	sleep(0.5)

	# Get into OSSI programming terminal
	tn.read_until("Terminal Type (513, 715, 4410, 4425, VT220, NTT, W2KTT, SUNT): [513] ")
	tn.write("ossi\n")
	sleep(0.5)

	# Check the trunk group list
	for trunkNumber in TRUNKS:
		tn.write("cstatus trunk " + trunkNumber + "\n")
		tn.write("t\n")
		sleep(0.5)
		parseOutput(tn.read_very_eager(), trunkNumber) 

	# Logoff OSSI
	tn.write("clogoff\n")
	tn.write("t\n")
	sleep(0.5)
	tn.write("y\n")
	
	# Exit
	sleep(0.5)
	tn.write("exit\n")

# Exit to Nagios	
exitToNagios(trunksBadList)