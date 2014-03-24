#!/bin/bash

/etc/init.d/kairos-redirector stop

if ! type chkconfig &> /dev/null; then
	update-rc.d -f kairos-redirector remove
else
	chkconfig kairos-redirector off
	chkconfig --del kairos-redirector
fi
