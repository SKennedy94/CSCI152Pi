#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

#TRIG = 11
#ECHO = 12
#TRIG2 = 15
#ECHO2 = 16
keyArray = [{'trigNumber': 11, 'echoNumber':12, 'description':'front sensor'}, {'trigNumber': 15, 'echoNumber':16, 'description':'back sensor'}]

def setup():
	GPIO.setmode(GPIO.BOARD)
	# This sets up the GPIO in and out pins. Using a for in loop
	for dictionaryObject in keyArray:
		# Sets up each trigNumber to GPIO.OUT
		GPIO.setup(dictionaryObject['trigNumber'], GPIO.OUT)
		# Sets up each echoNumber to GPIO.IN
		GPIO.setup(dictionaryObject['echoNumber'], GPIO.IN)

def distanceInMeters(trignum, echonum):
""" 
Calculates the distance of an ultrasonic sensor to an object.
@param {Integer} [trignum] The trigger number of the sensor.
@param {Integer} [echonum] The echo number of the sensor.
@return {Integer} [during] The distance of the sensor to object in distance.
"""
	GPIO.output(trignum, 0)
	time.sleep(0.000002)

	GPIO.output(trignum, 1)
	time.sleep(0.00001)
	GPIO.output(trignum, 0)

	
	while GPIO.input(echonum) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(echonum) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	distance = during * 340 / 2
	return distance

def loop():
	while True:
		for dictionaryObject in keyArray:
			#Calculates the distance
			distance = distanceInMeters(dictionaryObject['trigNumber'], dictionaryObject['echoNumber'])
			print 'Distance for ', dictionaryObject['description'], ': ', format(distance, '.3f') , 'm'
		print ''
		time.sleep(1)

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
