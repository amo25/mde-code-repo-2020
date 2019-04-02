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
	sleep(0.15) #need delay in order to give registers time to be written. 0.1 too small, may be able to go a bit faster than this
	subprocess.run(["sudo", "sh", "./PWM1_DC10.sh"])
	#subprocess.run(["sudo", "sh", "

def initPWM():
	subprocess.run(["sudo", "sh", "./PWM_0through7_INIT.sh"])
	#sleep(0.15) #don't seem to need delay for init? Keep an eye on this

initPWM()
#sleep(2)
takeImage()
