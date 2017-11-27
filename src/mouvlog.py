#!/usr/bin/python

import calendar, datetime, time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

path = '/root/data/'
tzoffset = calendar.timegm(datetime.datetime.now().timetuple()) - time.time()
filename = ''

files_limit = 1000 # max lines in file
files_lines = files_limit # init state

while True:
    GPIO.wait_for_edge(4, GPIO.BOTH)
    now = int((time.time() + tzoffset) * 1000)
    snow = str(now) + ',' + str(GPIO.input(4))
    if files_lines >= files_limit:
        filename = path + str(now) + '.txt'
        files_lines = 0
    with open(filename, "a") as myfile:
        myfile.write(snow+'\n')
    files_lines = files_lines + 1
