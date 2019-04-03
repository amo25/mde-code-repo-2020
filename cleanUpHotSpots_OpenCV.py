"""
*  This program interacts with the intel areo compute board.
*  The program is used to process and analyze the most
*  recent image taken from the flir vue thermal camera. From
*  there the largest hot spot is taken (b/c it's assumed to be
*  the closest).  And then the center of the hot spot is found
*  and the light is panned to the correct region and turned on
*  such that the light shines on the object.
*
*  Last edited: 4/2/2019
*  Authors: Liz Doggett, Alex Orlov, Bobbie Dee Kennedy
"""

import cv2
import numpy
import os



def mostRecentPhoto(passed_directory):
    """
    :param: directory
    :return: img_grey

     Specify the start Directory to search for the photos.
     Then searching via timestamps the most recent folder and image
     is pulled and converted to a grey scale image.
     """
    #searching from folder .... This will need to be changed to the E drive
    #directory='C:\VUE PRO 336'
    directory = passed_directory
    folders = []
    for d in os.listdir(directory):
        bd = os.path.join(directory, d)
        if os.path.isdir(bd): folders.append(bd)

    latest_img_dir = max(folders, key=os.path.getctime)
    latest_img_dir = latest_img_dir.replace('\\','/')
    #temp latest directory for testing
    #latest_img_dir = 'C:/VUE PRO 336/20190319_224041/'

    """ All the images in the most recent folder are stored into images[]"""
    images = []
    for img in os.listdir(latest_img_dir):
        img_path = os.path.join(latest_img_dir, img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if os.path.isdir(latest_img_dir):
            images.append(img_path)

    latest_img = max(images, key=os.path.getctime) #gets the most recent image for processing


    img_grey = cv2.imread(latest_img, flags=0) # reads in grey
    return(img_grey)

def processImage():
    """
    :return isolated_largest_contour


    Reads in most recent photot from mostRecentPhoto.
    Blurs the image to remove some of the noise and then
    converts the image to binary using a thershold.  Then
    the largest contour is found.
    """
    print("in process")
    img_grey = mostRecentPhoto('/media/alex/VUE PRO 336')

    #blurs the image
    blur_img = cv2.blur(img_grey, (10,5))

    size = blur_img.shape


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
    #closedFilter = cv2.morphologyEx(openingFilter, cv2.MORPH_CLOSE, kernel)


    #Trying connected components
    ret, labels = cv2.connectedComponents(openingFilter)


    contours, hierarchy = cv2.findContours(openingFilter, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    color = cv2.cvtColor(outputImg2, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(color, contours, -1, (0,0,255), 2)

    #Counting the number of countors
    contoursCount = len(contours)
    print("Number of Contours Detected: ", contoursCount)

    #Alex: TODO: if contoursCount > 0, turn on light
    #else, turn off light
    #once this works, set a minimum size for the contour and only turn on light if at least one of the contours is this size
    #finally, get the coordinates of the biggest contour and tilt light


    # Isolate largest contour
    if (contoursCount > 0):
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

        mask = numpy.zeros(openingFilter.shape, numpy.uint8)
        isolated_biggest_contour = cv2.drawContours(mask, [biggest_contour], -1, 255, -1)

        return(isolated_biggest_contour)
    else:
        return None

def locate_contour_x_coord(grey_image):
    """
    :param: isolated_bigest_countour
   
    Reads image which contains the largest contour of the orginal image.
    Then the center of the contour is found.  From there the image size is 
    taken and divided into 3rds.  The X cordinate of the center contour location
    is taken and used to dictate if the light should turn left, stay centered or turn right.
    """
    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(grey_image,127,255,0)

    # calculate moments of binary image
    M = cv2.moments(thresh)

    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # For debugging purposes this puts a dot in the center of the countour
    #   text and highlight the center
    # cv2.circle(grey_image, (cX, cY), 5, (125, 155, 155), -1)
    # cv2.putText(grey_image, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    height_img, width_img = grey_image.shape

    image_third = width_img//3 #The '//' does integer division
    print("cX " + str(cX))
    if(cX in range(1, image_third)):
        print("I'm in the first section")
    elif(cX in range(image_third, ((2*image_third)))):
        print("I'm in the middle")
    else:
        print("im in far right")

    # Use below lines for debugging
    #     It allows you to see gridded off image
    # cv2.line(grey_image, (image_third, 1), (image_third, height_img), (255,0,0), 1, 1)
    # cv2.line(grey_image, (2*image_third, 1), (2*image_third, height_img), (255,0,0), 1, 1)
    # cv2.imshow("Image", grey_image)
    # cv2.waitKey(0)
#
# if __name__ == '__main__':
largest_contour = processImage()
if (largest_contour != None):
    locate_contour_x_coord(largest_contour)
    #todo pan light in locate_con...
else:
    print("Debug remove")
