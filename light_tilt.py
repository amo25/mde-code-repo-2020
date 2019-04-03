#Light tilt test
import subprocess

def turnLightLeft():
    subprocess.run(["sudo", "sh", "./PWM2_DC_6_4_5.sh"])
    #todo add delay?
    
def turnLightRight():
    subprocess.run(["sudo", "sh", "./PWM2_DC_8_5_5.sh"])
    #todo add delay?
    
def turnLightCenter():
    subprocess.run(["sudo", "sh", "./PWM2_DC_7_5.sh"])
    #todo add delay?
    
turnLightRight()
