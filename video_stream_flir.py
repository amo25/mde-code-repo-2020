#Try this when NTSC to USB converter arrives
#Credit to: https://stackoverflow.com/questions/22146205/grab-frame-ntsctousb-dongle-opencv2-python-wrapper/22183737#22183737
#Note: Video 1 may already be taken by one of the Aero cameras (/dev/video1/)
#Check the code you installed on top of Ubuntu to make Aero cameras work

import cv2

cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_FFMPEG,True)
cam.set(cv2.CAP_PROP_FPS,30)

while(True):
    ret,frame = cam.read()
    cv2.imshow('frame',frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()
