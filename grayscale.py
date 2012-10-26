from cImage import *

def grayPixel(p):
    avg = (p.getRed() + p.getGreen() + p.getBlue()) // 3
    return Pixel(avg,avg,avg)

def makeGrayScale(imageFile):
    myimagewindow = ImageWin("Image Processing",600,200)
    oldimage = Image(imageFile)            
    oldimage.draw(myimagewindow)

    width = oldimage.getWidth()
    height = oldimage.getHeight()
    newim = EmptyImage(width,height)

    for row in range(height):
        for col in range(width):
            originalPixel = oldimage.getPixel(col,row)
            newPixel = grayPixel(originalPixel)
            newim.setPixel(col,row,newPixel)

    newim.setPosition(width+1,0)
    newim.draw(myimagewindow)
    myimagewindow.exitOnClick()

makeGrayScale('lcastle.gif')