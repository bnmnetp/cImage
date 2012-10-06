    
def double(oldimage):
    oldw = oldimage.getWidth()
    oldh = oldimage.getHeight()

    newim = EmptyImage(oldw*2,oldh*2)

    for row in range(newim.getWidth()):   #// \label{lst:dib1}
        for col in range(newim.getHeight()): #// \label{lst:dib2}
            
            originalCol = col//2  #// \label{lst:dib3}
            originalRow = row//2  #// \label{lst:dib4}
            oldpixel = oldimage.getPixel(originalCol,originalRow)

            newim.setPixel(col,row,oldpixel)

    return newim
