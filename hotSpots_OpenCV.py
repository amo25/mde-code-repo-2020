import cv2
import numpy
import os
from pathlib import Path
import imutils
from matplotlib import pyplot as plt

"""Okay so below gives way to get an 8 bit
grey scale image """
#searching from folder .... This will need to be changed to the E drive
directory='C:\VUE PRO 336'
folders = []
for d in os.listdir(directory):
    bd = os.path.join(directory, d)
    if os.path.isdir(bd): folders.append(bd)

latest_img_dir = max(folders, key=os.path.getctime)
print (latest_img_dir)
latest_img_dir = latest_img_dir.replace('\\','/')
print(latest_img_dir)
for img in os.listdir(latest_img_dir):
    print(img)
    img = os.path.join(latest_img_dir, img)
    img_grey = cv2.imread(img, flags=0) # reads in grey
    cv2.imshow("test", img_grey)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



#blurs the image
blur_img = cv2.blur(img_grey, (10,5))

size = blur_img.shape

blur_img_array = numpy.array(blur_img)
rows = size[0]
columns = size[1]

cv2.imshow("Blurred Image 1", blur_img)


hisEQ = cv2.equalizeHist(blur_img)
cv2.imshow("Historgram Equilization", (hisEQ))


#trying out thershold
retval2,threshold2 = cv2.threshold(img_grey,50,255,cv2.THRESH_BINARY)
cv2.imshow('original',img_grey)
cv2.imshow('threshold2',threshold2)

#Trying to fill in some spaces
th, im_th = cv2.threshold(threshold2,220,225,cv2.THRESH_BINARY_INV)
imgFloodFill = im_th.copy()
cv2.imshow("im_th", imgFloodFill)
h, w = im_th.shape[:2]
mask = numpy.zeros((h+2, w+2), numpy.uint8)
cv2.floodFill(imgFloodFill, mask, (0,0), 255)
invFloodFill = cv2.bitwise_not(imgFloodFill)
cv2.imshow("invFlood", invFloodFill)
ouputImg = im_th | invFloodFill

cv2.imshow("Filling1", ouputImg)

# plt.hist(ouputImg.ravel(), 256, [0,256])
# plt.show()

outputImg2 = cv2.threshold(ouputImg, 250, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("Trying", outputImg2)

#opening Filter
kernel = numpy.ones((3,3), numpy.uint8)
openingFilter = cv2.morphologyEx(outputImg2, cv2.MORPH_OPEN, kernel)
#closedFilter = cv2.morphologyEx(openingFilter, cv2.MORPH_CLOSE, kernel)
cv2.imshow("Open Filter", openingFilter)


#Trying connected components
ret, labels = cv2.connectedComponents(openingFilter)


contours, hierarchy = cv2.findContours(openingFilter, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
color = cv2.cvtColor(outputImg2, cv2.COLOR_GRAY2RGB)
cv2.drawContours(color, contours, -1, (0,0,255), 2)
cv2.imshow("Contours", color)


#Counting the number of countors
contoursCount = len(contours)
print("Number of Contours Detected: ", contoursCount)

#Alex: TODO: if contoursCount > 0, turn on light
#else, turn off light
#once this works, set a minimum size for the contour and only turn on light if at least one of the contours is this size
#finally, get the coordinates of the biggest contour and tilt light


# Isolate largest contour
contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

mask = numpy.zeros(openingFilter.shape, numpy.uint8)
cv2.drawContours(mask, [biggest_contour], -1, 255, -1)

cv2.imshow('Biggest Contour', mask)

# largest_area = 0
# largest_countour_index = 0
# cnt = contours[0]
# areas = []
# for cnt in contours:
#     # area = cv2.contourArea(cnt)
#     areas.append(cv2.contourArea(cnt))
#
# sorted_areas = sorted(zip(areas, contours), key=lambda  x: x[0], reverse=True)
# if sorted_areas and len(sorted_areas) >= 10:
#     print (sorted_areas[10 - 1][1])
# else:
#     print(None)
    # if (area>largest_area):
    #     largest_area=area
    #     largest_contour_index=cnt
    #     bounding_rect=cv2.boundingRect(contours[cnt])
# rect=img_grey(bounding_rect).clone()
# cv2.imshow('largest contour ',rect)


cv2.waitKey(0)