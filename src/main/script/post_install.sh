#!/bin/bash

if ! type chkconfig &> /dev/null; then
	update-rc.d kairos-redirector defaults
else
	chkconfig --add kairos-redirector
	chkconfig kairos-redirector on
fi

/etc/init.d/kairos-redirector start
