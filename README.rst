cImage  -  A simple image processing library for Python
=======================================================


Installation
============

copy cImage.py to your site-packages directory.


Usage
=====

This image library is not going to give you fancy high performance operations on images.  It allows you to read in an image and manipulate its pixels.  Then you can save the new image to a file, or you can display the image in a window.  Thats really about it, but its really all you want to do if you are teaching an introductory computer science course.

Image Types Supported
---------------------

If you have PIL installed on your system:

* jpeg
* gif
* tiff
* png
* etc.

If you do not have PIL installed then you are stuck with GIF images only.

If you are using Python 2.6/2.7 I recommend you install Pillow its a simple fork
of PIL that you can install with easy_install or pip.

If you are using Python 3 You can get a working version of PIL
Here:  https://pypi.python.org/pypi/Pillow/2.0.0

Note that if you scroll down to the bottom you will find binary installations for Windows.  Linux and Mac users can follow the instructions on the page.


Example
-------

::

    from cImage import *
    myimagewindow = ImageWin("Image Processing",600,300)
    oldimage = FileImage("lutherbell.jpg")
    oldimage.setPosition(0,0)
    oldimage.draw(myimagewindow)

    width = oldimage.getWidth()
    height = oldimage.getHeight()
    newim = EmptyImage(width,height)

    for row in range(height):
    	for col in range(width):
    		oldpixel = oldimage.getPixel(col,row)
    		ave=(oldpixel.getRed()+oldpixel.getGreen()+oldpixel.getBlue())/3
    		newim.setPixel(col,row,Pixel(ave,ave,ave))

    newim.setPosition(width+1,0)
    newim.draw(myimagewindow)

    myimagewindow.exitOnClick()
