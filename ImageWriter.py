import media
import color
##
# This function loads the image name passed in.
# The function will pass back a reference to the
# picture which needs to be stored for any future processing.
# This function will not show the image 
def loadPicture(filename):
    pic = media.load_picture(filename)
    return pic
##
# This function shows the image passed in as parameter. 
def showPicture(pic):
    pic.show()
    
##
# If any changes are made to the picture,
# the changes are not displayed on the image being shown
# until this function is called.
def updatePicture(pic):
    media.update(pic)

##
# This function will save the picture passed in as a file
# using the name passed in the variable filename.
# Make sure that the string filename has the proper
# file extension for an image. File names can have
# extensions "gif", "jpg", "bmp".
def savePicture(pic,filename):
    media.save_as(pic,filename)

##
# This function returns the width of the picture as an integer.
def getWidth(pic):
    return media.get_width(pic)

##
# This function returns the height of the picture as an integer.
def getHeight(pic):
    return media.get_height(pic)

##
# This function returns the color at location x, y of the picture.
# The color is returned as a list of three values
# representing the red, green, and blue component of the color.
def getColor(pic,x,y):
    if getWidth(pic) > x and getHeight(pic) > y:
        pix = media.get_pixel(pic,x,y)
        clr = media.get_color(pix)
        return list(clr.get_rgb())
    else:
        return None
##
# Sets the color of the location x, y to color passed in.
# The color is a list of three elements representing the
# red, green, and blue component of the color
def setColor(pic,x,y,col):
    if len(col) == 3:
        clr = color.Color(col[0],col[1],col[2])
        if getWidth(pic) > x and getHeight(pic) > y:
            pix = media.get_pixel(pic,x,y)
            media.set_color(pix,clr)
            

    
