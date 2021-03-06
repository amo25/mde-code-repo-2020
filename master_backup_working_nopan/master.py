#Main logic for MDE Drone Team 2019 coyote detection
#Connect light on/off to PWM0, camera to PWM1, and light servo to PWM2
#Must be run as superuser
#Ensure light starts in state 0 (off, where the next state is a solid light)
#Currently, PWM0 assigned to N1 (Pin 3 from left), PWM1 to P2 (Pin 2 from left), and PWM2 to L4 (Pin 4 from left)

#todo direct OpenCV access to camera
#todo link FPGA and FC
#todo incorporate MAVlink control to pause the drone
#todo turn on light for a few seconds, turn off, then take another image
#todo take images with light turned off and on at night
#todo regulate light supply voltage

import cv2
import numpy
import os
import imutils
import subprocess
from time import sleep

def turnOnLight():
	subprocess.run(["sudo", "sh", "./PWM0_DC5.sh"])
	subprocess.run(["sudo", "sh", "./PWM0_DC10.sh"])

def turnOffLight():
	subprocess.run(["sudo", "sh", "./PWM0_DC5.sh"])
	subprocess.run(["sudo", "sh", "./PWM0_DC10.sh"])
	subprocess.run(["sudo", "sh", "./PWM0_DC5.sh"])

def takeImage():
	subprocess.run(["sudo", "sh", "./PWM1_DC5.sh"])
	sleep(0.15)
	subprocess.run(["sudo", "sh", "./PWM1_DC10.sh"])
	sleep(10) #need to wait for image to be taken and be recognized by os

def initPWM():
	subprocess.run(["sudo", "sh", "./PWM_0through7_INIT.sh"])
	sleep(0.15)

#init
initPWM();
#hardcoded directory path
directory='/media/alex/VUE PRO 336'
folders = []

#keep taking pictures, about 1 every 10 seconds
while(True):
	takeImage();

	"""Okay so below gives way to get an 8 bit
	grey scale image """
	for d in os.listdir(directory):
		bd = os.path.join(directory, d)
		if os.path.isdir(bd): folders.append(bd)

	latest_img_dir = max(folders, key=os.path.getctime)
	print (latest_img_dir)

	""" All the images in the most recent folder are stored into images[]"""
	images = []
	for img in os.listdir(latest_img_dir):
		img_path = os.path.join(latest_img_dir, img)

		if os.path.isdir(latest_img_dir):
			images.append(img_path)

	latest_img = max(images, key=os.path.getctime) #gets the most recent image for processing


	img_grey = cv2.imread(latest_img, flags=0) # reads in grey


	#blurs the image
	blur_img = cv2.blur(img_grey, (10,5))

	size = blur_img.shape

	blur_img_array = numpy.array(blur_img)
	rows = size[0]
	columns = size[1]


	#trying out thershold
	retval2,threshold2 = cv2.threshold(img_grey,50,255,cv2.THRESH_BINARY)

	#Trying to fill in some spaces
	th, im_th = cv2.threshold(threshold2,220,225,cv2.THRESH_BINARY_INV)
	imgFloodFill = im_th.copy()
	h, w = im_th.shape[:2]
	mask = numpy.zeros((h+2, w+2), numpy.uint8)
	cv2.floodFill(imgFloodFill, mask, (0,0), 255)
	invFloodFill = cv2.bitwise_not(imgFloodFill)
	ouputImg = im_th | invFloodFill

	outputImg2 = cv2.threshold(ouputImg, 250, 255, cv2.THRESH_BINARY)[1]

	#opening Filter
	kernel = numpy.ones((3,3), numpy.uint8)
	openingFilter = cv2.morphologyEx(outputImg2, cv2.MORPH_OPEN, kernel)


	#Trying connected components
	ret, labels = cv2.connectedComponents(openingFilter)


	contours, hierarchy = cv2.findContours(openingFilter, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#color = cv2.cvtColor(outputImg2, cv2.COLOR_GRAY2RGB)
	#cv2.drawContours(color, contours, -1, (0,0,255), 2)


	#Counting the number of countors
	contoursCount = len(contours)
	print("Number of Contours Detected: ", contoursCount)

	#Alex: TODO if contoursCount > 0, turn on light
	#else, turn off light
	#once this works, set a minimum size for the contour and only turn on light if at least one of the contours is this size
	#finally, get the coordinates of the biggest contour and tilt light
	if (contoursCount > 0):
		turnOnLight();
		# Isolate largest contour
		contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
		biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

		mask = numpy.zeros(openingFilter.shape, numpy.uint8)
		show_biggest_contour = cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
	else:
		turnOffLight();
