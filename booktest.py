import cImage as image

img = image.Image("lcastle.gif")
newimg = image.EmptyImage(img.getWidth(),img.getHeight())
win = image.ImageWin()

for col in range(img.getWidth()):
    for row in range(img.getHeight()):
       p = img.getPixel(col,row)

       newred = 255-p.getRed()
       newgreen = 255-p.getGreen()
       newblue = 255-p.getBlue()

       newpixel = image.Pixel(newred,newgreen,newblue)

       newimg.setPixel(col,row,newpixel)

newimg.draw(win)
win.exitonclick()