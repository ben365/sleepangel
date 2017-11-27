#!/bin/bash

cd /home/pi/sleepangel/

#http://pi.gadgetoid.com/pinout

# set volume
amixer -q set PCM 90%
# activate speaker with relay
gpio mode 0 out
gpio write 0 1
# play sound with infinite loop
/usr/bin/mpg123 -q -D 2 --loop -1 ./sonnerie.mp3 & 
PID1=$!
# wait for button push
nc -l -U /tmp/alarm_button > /dev/null
# desactivate speaker with relay
gpio write 0 0
# kill sound player
kill -9 $PID1
