#!/bin/bash

pipe=/var/log/kairos/metrics

# Current time in milliseconds
now=$(($(date +%s%N)/1000000))

metric=redirect_load_avg
value=`cat /proc/loadavg | cut -d ' ' -f 1`

if [ -p $pipe ]
then
	echo -e "$metric $now $value host=$HOSTNAME\n" > $pipe
fi
