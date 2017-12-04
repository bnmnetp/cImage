cImage  -  A simple image processing library for Python
=======================================================


Installation
============


If using Thonny, go to Tools -> Manage Packages, then enter ``cs20-image``. This should install both the image module, and the Pillow module (so you can use any type of image you'd like).


If you are not using Thonny, copy image.py to your site-packages directory, or just keep it in the same folder as the Python scripts that import it.


Usage
=====

This image library is not going to give you fancy high performance operations on images.  It allows you to read in an image and manipulate its pixels.  Then you can save the new image to a file, or you can display the image in a window.  Thats really about it, but its really all you want to do if you are teaching an introductory computer science course.

Image Types Supported
---------------------

If you have PIL installed on your system (if you are using Thonny, this was installed along with the image module):

* jpeg
* gif
* tiff
* png
* etc.

If you do not have PIL installed then you are stuck with GIF images only.


Example
-------

::

    import image

    win = image.ImageWin(480, 640, "Image Processing")
    original_image = image.FileImage('lcastle.gif')

    width = original_image.get_width()
    height = original_image.get_height()
    print(width, height)

    original_image.draw(win)
    my_image = original_image.copy()

    for row in range(height):
        for col in range(width):
             v = my_image.get_pixel(col,row)
             v.red = 255 - v.red
             v.green = 255 - v.green
             v.blue = 255 - v.blue
             my_image.set_pixel(col,row,v)

    my_image.draw(win)
    print(win.get_mouse())
    my_image.save('lcastle-inverted.gif')
    print(my_image.to_list())
    win.exit_on_click()
