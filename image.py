"""
image.py
This module provides a simple interface to create a window, load an image and experiment
with image based algorithms.  Many of which require pixel-by-pixel manipulation.  This
is a educational module, its not intended to replace the excellent Python Image Library, in fact
it uses PIL.

The module and its interface and some of the code were inspired/copied by/from John Zelle's graphics.py
which serves a similar purpose in the graphics primitive world.
"""

# Release Notes:
# Version 1.0   Fall 2005
#
# Brad Miller, Luther College
#
# Version 1.1   December 7, 2005
# Changes:
#   Modify class name for base image to be AbstractImage   This way we don't have a lower case
#      class name running around.  We still don't expect people to create an AbstractImage but
#      rather create an image through FileImage, ListImage, or EmptyImage.
#   Add ability to convert an image to a list
#   Add save function to write an image back to disk.
#
# Version 1.2  November 2007
# Changes:
#  Modify the setPosition function to position the image by the top left corner rather than
#    the center.
#  Add the exitOnClick method to ImageWin.  Use this as the last call in the program to
#    avoid early exits when running from the command line, and nasty hangs when running
#    from within IDLE
#
# Version 1.3  May 2008
# Changes:
#   Modify all code to be Python 3.0 ready.  -- still runs under 2.x
#   Modify all code so that if PIL is not available then image.py will still
#   function using Tkimages.  N.B.  Tk restricts image types to gif or ppm
#
# Andrew Mertz, Eastern Illinois University
# October 2014
# Changes:
#   Negative indices can be used in Pixel's  __getitem__ function
#   Pixel's __getitem__ function now supports looping i.e. for value in Pixel(0, 1, 2):
#
# Giovanni Moretti, Massey University, Palmerston North, New Zealand
# April 2015
# Changes:
# Added _imroot.lift() to ensure that pictures aren't hidden under other Windows
# (needed on Windows 7 & Python 3.4. Ubuntu 14.04 was fine without it).
#
# version 1.4
# Brad Miller
# distribute on pypi
#
# Dan Schellenberg
# Dec 2017
# Changes:
#   Add setDelay function stub to avoid code copied from Runestone-type textbook examples to crash
#   Reorder parameters for ImageWin constructor, so Runestone-type examples behave without window name
#   Added underscore_separated_function_calls to allow for either mixedCase or under_score calls
#
# Dan Schellenberg
# Apr 2018
# Changes:
#   Force the Pixel object to store all rgb values as int's, to avoid students getting errors when
#       they divide in their image manipulation calculations
#   Make EmptyImage's show up with white backgrounds, for both PIL and tkinter
# Version 1.5 May 2016 Max Hailperin <max@gustavus.edu>
# Changes:
#   Add more checks of parameter types and ranges so error messages are
#     closer to the user's code and more intelligible.
#   Disable the ability of Pixels to range up to 1.0 instead of 255, which
#     didn't seem used and would make the type checking more complex.
#
# Version 1.6 May 2016 Max Hailperin <max@gustavus.edu>
# Changes:
#   Add autoShow function that can be used to get and optionally set a flag
#     that if True makes images automatically be displayed when their printed
#     representation is produced (e.g. as results in the shell).

try:
    import tkinter
except:
    import Tkinter as tkinter

pilAvailable = True
try:
    from PIL import Image as PIL_Image
    from PIL import ImageTk
except:
    pilAvailable = False

#import exceptions

# Borrow some ideas from Zelle
# create an invisible global main root for all windows
tk = tkinter
_imroot = tk.Tk()
_imroot.withdraw()

# Make sure the displayed window is on top - otherwise drawing can appear to fail.
# The _imroot.lift() call was required on Windows 7 - Linux was fine without it
# not sure about Mac, but there are some tips at
# http://stackoverflow.com/questions/8691655/how-to-put-a-tkinter-window-on-top-of-the-others
_imroot.lift()
#_imroot.call('wm', 'attributes', '.', '-topmost', True)
#_imroot.after_idle(_imroot.call, 'wm', 'attributes', '.', '-topmost', False)


# For backward compatibility, the new autoShow feature is off by default:
autoShowOn = False

def autoShow(newSetting=None):
    """Return and optionally change the True/False autoShow setting"""
    global autoShowOn
    oldSetting = autoShowOn
    if newSetting != None:
        autoShowOn = newSetting
    return oldSetting

def formatPixel(data):
    if type(data) == tuple:
        return '{#%02x%02x%02x}'%data
    elif isinstance(data,Pixel):
        return '{#%02x%02x%02x}'%data.getColorTuple()

class ImageWin(tk.Canvas):
    """
    ImageWin:  Make a frame to display one or more images.
    """
    def __init__(self,width=640,height=640,title="image window"):
        """
        Create a window with a title, width and height.
        """
        master = tk.Toplevel(_imroot)
        master.protocol("WM_DELETE_WINDOW", self._close)
        #super(ImageWin, self).__init__(master, width=width, height=height)
        tk.Canvas.__init__(self, master, width=width, height=height)
        self.master.title(title)
        self.pack()
        master.resizable(0,0)
        self.foreground = "white"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self.bind("<Button-1>", self._onClick)
        self.height = height
        self.width = width
        self._mouseCallback = None
        self.trans = None
        _imroot.update()

    def _close(self):
        """Close the window"""
        self.master.destroy()
        self.quit()
        _imroot.update()

    def getMouse(self):
        """Wait for mouse click and return a tuple with x,y position in screen coordinates after
        the click"""
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            self.update()
        return ((self.mouseX,self.mouseY))

    def get_mouse(self):
        return self.getMouse()

    def setMouseHandler(self, func):
        self._mouseCallback = func

    def set_mouse_handler(self, func):
        self.setMouseHandler(func)

    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self._mouseCallback:
            self._mouseCallback(e.x, e.y)

    def _on_click(self, e):
        self._onClick(e)

    def exitOnClick(self):
        """When the Mouse is clicked close the window and exit"""
        self.getMouse()
        self._close()

    def exitonclick(self):
        self.exitOnClick()

    def exit_on_click(self):
        self.exitOnClick()

class Pixel(object):
    """This simple class abstracts the RGB pixel values."""
    def __init__(self, red, green, blue):
        super(Pixel, self).__init__()
        self.max = 255
        self.setRed(red)
        self.setGreen(green)
        self.setBlue(blue)

    def getRed(self):
        """Return the red component of the pixel"""
        return int(self.__red)

    def get_red(self):
        return self.getRed()

    def getGreen(self):
        """Return the green component of the pixel"""
        return int(self.__green)

    def get_green(self):
        return self.getGreen()

    def getBlue(self):
        """Return the blue component of the pixel"""
        return int(self.__blue)

    def get_blue(self):
        return self.getBlue()

    def getColorTuple(self):
        """Return all color information as a tuple"""
        return (int(self.__red), int(self.__green), int(self.__blue))

    def get_color_tuple(self):
        return self.getColorTuple()

    def setRed(self,red):
        """Modify the red component"""
        if not isinstance(red, int):
            raise TypeError("Error:  pixel value %r is not an integer" % red)
        elif self.max >= red >= 0:
            self.__red = red
        else:
            raise ValueError("Error:  pixel value %d is out of range" % red)

    def set_red(self, red):
        self.setRed(red)

    def setGreen(self,green):
        """Modify the green component"""
        if not isinstance(green, int):
            raise TypeError("Error:  pixel value %r is not an integer" % green)
        elif self.max >= green >= 0:
            self.__green = green
        else:
            raise ValueError("Error:  pixel value %d is out of range" % green)

    def set_green(self, green):
        self.setGreen(green)

    def setBlue(self,blue):
        """Modify the blue component"""
        if not isinstance(blue, int):
            raise TypeError("Error:  pixel value %r is not an integer" % blue)
        elif self.max >= blue >= 0:
            self.__blue = blue
        else:
            raise ValueError("Error:  pixel value %d is out of range" % blue)

    def set_blue(self, blue):
        self.setBlue(blue)

    def __getitem__(self,key):
        """Allow new style pixel class to act like a color tuple:
           0 --> red
           1 --> green
           2 --> blue
        """
        if isinstance(key, slice):
            raise TypeError("Slicing is not supported")
        if key == 0 or key == -3:
            return self.__red
        elif key == 1 or key == -2:
            return self.__green
        elif key == 2 or key == -1:
            return self.__blue
        else:
            raise IndexError("Error %d Index out of range" % key)

    def setRange(self,pmax):
        """docstring for setRange"""
        if pmax == 1.0:
            raise ValueError("Range of 1.0 is not currently supported")
            # This raising of an error was inserted  in conjunction with
            # requiring the values to be integers, which is necessary for
            # formatPixel to work correctly. Was 1.0 ever used?
            self.max = 1.0
        elif pmax == 255:
            self.max = 255
        else:
            raise ValueError("Error range must be 1.0 or 256")

    def set_range(self, pmax):
        self.setRange(pmax)

    def __str__(self):
        return str(self.getColorTuple())

    def __repr__(self):
        """docstring for __repr__"""
        return str(self.getColorTuple())

    red = property(getRed, setRed, None, "I'm the red property.")
    green = property(getGreen, setGreen, None, "I'm the green property.")
    blue = property(getBlue, setBlue, None, "I'm the blue property.")

class AbstractImage(object):
    """
    Create an image.  The image may be created in one of four ways:
    1. From an image file such as gif, jpg, png, ppm  for example: i = image('fname.jpb)
    2. From a list of lists
    3. From another image object
    4. By specifying the height and width to create a blank image.
    """
    imageCache = {} # tk photoimages go here to avoid GC while drawn
    imageId = 1

    def __init__(self,fname=None,data=[],imobj=None,height=0,width=0):
        """
        An image can be created using any of the following keyword parameters. When image creation is
        complete the image will be an rgb image.
        fname:  A filename containing an image.  Can be jpg, gif, and others
        data:  a list of lists representing the image.  This might be something you construct by
        reading an asii format ppm file, or an ascii art file and translate into rgb yourself.
        imobj:  Make a copy of another image.
        height:
        width: Create a blank image of a particular height and width.
        """
        super(AbstractImage, self).__init__()

        # if PIL is available then use the PIL functions otherwise fall back to Tk
        if pilAvailable:
            self.loadImage = self.loadPILImage
            self.createBlankImage = self.createBlankPILImage
            self.setPixel = self.setPILPixel
            self.set_pixel = self.setPILPixel
            self.getPixel = self.getPILPixel
            self.get_pixel = self.getPILPixel
            self.save = self.savePIL
        else:
            self.loadImage = self.loadTkImage
            self.createBlankImage = self.createBlankTkImage
            self.setPixel = self.setTkPixel
            self.set_pixel = self.setTkPixel
            self.getPixel = self.getTkPixel
            self.get_pixel = self.getTkPixel
            self.save = self.saveTk

        if fname:
            self.loadImage(fname)
            self.imFileName = fname
        elif data:
            height = len(data)
            width = len(data[0])
            self.createBlankImage(height,width)
            for row  in range(height):
                for col in range(width):
                    self.setPixel(col,row,Pixel(data[row][col]))
        elif height > 0 and width > 0:
            self.createBlankImage(height,width)
        elif imobj:
            self.im = imobj.copy()

        if pilAvailable:
            self.width,self.height = self.im.size
        else:
            self.width = self.im.width()
            self.height = self.im.height()
        self.centerX = self.width/2+3     # +3 accounts for the ~3 pixel border in Tk windows
        self.centerY = self.height/2+3
        self.id = None

    def setDelay(self, delay=0, interval=0):
        """Just a stub so that programs copy/pasted from an online textbook do not crash."""
        print("The setDelay function is not implemented in this version of the image module. " \
              "To animate your code, put img.draw(win) inside your nested loop, indented the " \
              "same amount as the inner loop.")

    def set_delay(self, delay=0, interval=0):
        self.setDelay(delay, interval)

    def loadPILImage(self,fname):
        self.im = PIL_Image.open(fname)
        ni = self.im.convert("RGB")
        self.im = ni

    def loadTkImage(self,fname):
        sufstart = fname.rfind('.')
        if sufstart < 0:
            suffix = ""
        else:
            suffix = fname[sufstart:]
        if suffix not in ['.gif', '.ppm']:
            raise ValueError("Bad Image Type: %s : Without PIL, only .gif or .ppm files are allowed" % suffix)
        self.im = tkinter.PhotoImage(file=fname)

    def createBlankPILImage(self,height,width):
        self.im = PIL_Image.new("RGB",(width,height), (255, 255, 255))
        ni = self.im.convert("RGB")
        self.im = ni

    def createBlankTkImage(self,height,width):
        self.im = tkinter.PhotoImage(height=height,width=width)
        hexcode = "#%02x%02x%02x" % (255,255,255)
        horizontal_line = "{" + " ".join([hexcode]*width) + "}"
        self.im.put(" ".join([horizontal_line]*height))

    def copy(self):
        """Return a copy of this image"""
        newI = AbstractImage(imobj=self.im)
        return newI


    def clone(self):
         """Return a copy of this image"""
         newI = AbstractImage(imobj=self.im)
         return newI

    def getHeight(self):
        """Return the height of the image"""
        return self.height

    def get_height(self):
        return self.height

    def getWidth(self):
        """Return the width of the iamge"""
        return self.width

    def get_width(self):
        return self.width

    def getTkPixel(self,x,y):
        """Get a pixel at the given x,y coordinate.  The pixel is returned as an rgb color tuple
        for example foo.getPixel(10,10) --> (10,200,156) """
        p = self.im.get(x,y)
        # p is a string in some tkinter versions; tuple in others.
        try:
            p = [int(j) for j in p.split()]
        except AttributeError:
            pass
        return Pixel(p[0],p[1],p[2])

    def setTkPixel(self,x,y,pixel):
        """Set the color of a pixel at position x,y.  The color must be specified as an rgb tuple (r,g,b) where
        the rgb values are between 0 and 255."""
        if x < self.getWidth() and y < self.getHeight():
            self.im.put(formatPixel(pixel.getColorTuple()),(x,y))
        else:
            raise ValueError("Pixel index out of range.")

    def getPILPixel(self,x,y):
        """docstring for getPILPIxel"""
        p = self.im.getpixel((x,y))
        return Pixel(p[0],p[1],p[2])

    def setPILPixel(self,x,y,pixel):
        """docstring for setPILPixel"""
        if x < self.getWidth() and y < self.getHeight():
            self.im.putpixel((x,y),pixel.getColorTuple())
        else:
            raise ValueError("Pixel index out of range")

    def setPosition(self,x,y):
        """Set the position in the window where the top left corner of the window should be."""
        self.top = y
        self.left = x
        self.centerX = x + (self.width/2)+3
        self.centerY = y + (self.height/2)+3

    def set_postion(self, x, y):
        self.setPosition(x, y)

    def getImage(self):
        if pilAvailable:
            return ImageTk.PhotoImage(self.im)
        else:
            return self.im

    def draw(self,win):
        """Draw this image in the ImageWin window."""
        ig = self.getImage()
        self.imageCache[self.imageId] = ig # save a reference else Tk loses it...
        AbstractImage.imageId = AbstractImage.imageId + 1
        self.canvas=win
        self.id = self.canvas.create_image(self.centerX,self.centerY,image=ig)
        _imroot.update()

    def saveTk(self,fname=None,ftype='gif'):
        if fname == None:
            fname = self.imFileName
        sufstart = fname.rfind('.')
        if sufstart < 0:
            suffix = ""
        else:
            suffix = fname[sufstart:]
        if suffix == "":
            suffix = "."+ftype
            fname = fname+suffix
        if suffix not in ['.gif', '.ppm']:
            raise ValueError("Without PIL, only .gif or .ppm files are allowed")
        try:
            self.im.write(fname,format=ftype)
        except IOError as e:
            print(e)
            print("Error saving, Could Not open ", fname, " to write.")
        except tkinter.TclError as tke:
            print(tke)
            print("gif files can only handle 256 distinct colors")

    def savePIL(self,fname=None,ftype='jpg'):
        if fname == None:
            fname = self.imFileName
        sufstart = fname.rfind('.')
        if sufstart < 0:
            suffix = ""
        else:
            suffix = fname[sufstart:]
        if suffix == "":
            suffix = "."+ftype
            fname = fname+suffix
        try:
            self.im.save(fname)
        except:
            print("Error saving, Could Not open ", fname, " to write.")


    def toList(self):
        """
        Convert the image to a List of Lists representation
        """
        res = []
        for i in range(self.height):
            res.append([])
            for j in range(self.width):
                res[i].append(self.getPixel(j,i))
        return res

    def to_list(self):
        return self.toList()

    def __repr__(self):
        r = super(AbstractImage, self).__repr__()
        if autoShowOn:
            w = ImageWin(r, self.width, self.height)
            self.draw(w)
        return r


class FileImage(AbstractImage):
    def __init__(self,thefile):
        if not isinstance(thefile, str):
            raise TypeError("Error: file name %r not a string" % thefile)
        super(FileImage, self).__init__(fname = thefile)

class Image(FileImage):
        pass

class EmptyImage(AbstractImage):
    def __init__(self,cols,rows):
        if not isinstance(cols, int):
            raise TypeError("Error: width %r not an integer" % cols)
        if cols <= 0:
            raise ValueError("Error: width %d not positive" % cols)
        if not isinstance(rows, int):
            raise TypeError("Error: height %r not an integer" % rows)
        if rows <= 0:
            raise ValueError("Error: height %d not positive" % rows)
        super(EmptyImage, self).__init__(height = rows, width = cols)

class ListImage(AbstractImage):
    def __init__(self,thelist):
        # Note that the corresponding code in AbstractImage doesn't work
        # so apparently ListImage isn't used. As such, there doesn't seem
        # to be much point in adding error checking.
        super(ListImage, self).__init__(data=thelist)

# Example program  Read in an image and calulate the negative.
if __name__ == '__main__':
    win = ImageWin(480, 640, "Image Processing")
    original_iamge = FileImage('lcastle.gif')

    width = original_iamge.get_width()
    height = original_iamge.get_height()
    print(width, height)

    original_iamge.draw(win)
    my_image = original_iamge.copy()

    for row in range(height):
        for col in range(width):
             v = my_image.get_pixel(col,row)
             v.red = 255 - v.red
             v.green = 255 - v.green
             v.blue = 255 - v.blue
#             x = map(lambda x: 255-x, v)
             my_image.set_pixel(col,row,v)

    my_image.draw(win)
    print(win.get_mouse())
    my_image.save('lcastle-inverted.gif')
    print(my_image.to_list())
    win.exit_on_click()
