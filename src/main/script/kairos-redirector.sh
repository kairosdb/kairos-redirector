#!/bin/bash

# Find the location of the bin directory and change to the root of kairosdb
REDIRECTOR_BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$REDIRECTOR_BIN_DIR/.."

REDIRECTOR_LIB_DIR="lib"
REDIRECTOR_LOG_DIR="log"

if [ ! -d "$REDIRECTOR_LOG_DIR" ]; then
	mkdir "$REDIRECTOR_LOG_DIR"
fi

if [ "$KAIROS_PID_FILE" = "" ]; then
	KAIROS_PID_FILE=/var/run/kairosdb.pid
fi

export PYTHONPATH="$REDIRECTOR_BIN_DIR/../lib"

if [ "$1" = "run" ] ; then
	shift
	exec python lib/start.py conf/redirector.ini
elif [ "$1" = "start" ] ; then
	shift
	exec python lib/start.py conf/redirector.ini >> "$REDIRECTOR_LOG_DIR/redirector.log" 2>&1 &
	echo $! > "$KAIROS_PID_FILE"
elif [ "$1" = "stop" ] ; then
	shift
	kill `cat $KAIROS_PID_FILE` > /dev/null 2>&1
	while kill -0 `cat $KAIROS_PID_FILE` > /dev/null 2>&1; do
		echo -n "."
		sleep 1;
	done
	rm $KAIROS_PID_FILE
else
	echo "Unrecognized command."
	exit 1
fi
