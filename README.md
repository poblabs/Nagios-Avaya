# Nagios Avaya checks
=============

(c) Pat O'Brien <poblabs@github.com> - http://github.com/poblabs
Please read LICENSE for licensing info

These are a collection of scripts used for Nagios and checking Avaya alarms, trunk groups and server health. 

`check_avaya_alarms.sh`: This script uses `sshpass` to SSH into the Avaya CM, and gets a list of the alarms that are present. If any are present, it alerts Nagios.

`check_avaya_trunks.py`: This script takes the list of trunk groups to check, and logs into the Avaya CM, uses OSSI programming to get trunk status. If any are out of service, it alerts Nagios.

`check_avaya_uptime.sh`: This script uses `sshpass` to SSH into the Avaya CM, get the uptime and compare it against a threshold you define. If the uptime is over a threshold, it alerts Nagios.
