
# py_kohn_bmp - Copyright 2007 by Michael Kohn
# http://www.mikekohn.net/
# mike@mikekohn.net
#
# Feel free to use this class in your own programs (commerical or not)
# as long as you don't remove my name, email address, webpage, or copyright.
#
# Example how to use:
#
# my_bmp.kohn_bmp("out.bmp",image_width,image_height,3) <-- depth of 3 is color
# my_bmp.write_pixel(red,green,blue)  <-- do this width*height times
# my_bmp.close()
#
# if depth is set to 1 (black and white image) call write_pixel_bw(y) where
# y is between 0 and 255

# adapted by Antonio Cuni - 2010

from cStringIO import StringIO

class kohn_bmp:
  out=0
  width=0
  height=0
  depth=0
  bytes=0
  xpos=0
  width_bytes=0

  def write_int(self,n):
    str_out='%c%c%c%c' % ((n&255),(n>>8)&255,(n>>16)&255,(n>>24)&255)
    self.out.write(str_out)

  def write_word(self,n):
    str_out='%c%c' % ((n&255),(n>>8)&255)
    self.out.write(str_out)

  def __init__(self,width,height,depth):
    self.width=width
    self.height=height
    self.depth=depth

    self.width_bytes=width*depth
    if (self.width_bytes%4)!=0:
      self.width_bytes=self.width_bytes+(4-(self.width_bytes%4))

    self.out=StringIO()
    self.out.write("BM")          # magic number
    if depth==1:
      self.write_int((self.width_bytes*height)+54+1024)
    else:
      self.write_int((self.width_bytes*height)+54)
    self.write_word(0)
    self.write_word(0)
    if depth==1:
      self.write_int(54+1024)
    else:
      self.write_int(54)

    self.write_int(40)                 # header_size
    self.write_int(width)              # width
    self.write_int(height)             # height
    self.write_word(1)                 # planes
    self.write_word(depth*8)           # bits per pixel
    self.write_int(0)                  # compression
    self.write_int(self.width_bytes*height*depth) # image_size
    self.write_int(0)                  # biXPelsperMetre
    self.write_int(0)                  # biYPelsperMetre

    if depth==1:
      self.write_int(256)              # colors used
      self.write_int(256)              # colors important

      for c in range(256):
        self.out.write('%c' % c)
        self.out.write('%c' % c)
        self.out.write('%c' % c)
        self.out.write('%c' % 0)

    else:
      self.write_int(0)                # colors used - 0 since 24 bit
      self.write_int(0)                # colors important - 0 since 24 bit


  def write_pixel_bw(self,y):
    self.out.write(str("%c" % y))
    self.xpos=self.xpos+1
    if self.xpos==self.width:
      while self.xpos<self.width_bytes:
        self.out.write(str("%c" % 0))
        self.xpos=self.xpos+1
      self.xpos=0

  def write_pixel(self,red,green,blue):
    self.out.write(str("%c" % (blue&255)))
    self.out.write(str("%c" % (green&255)))
    self.out.write(str("%c" % (red&255)))
    self.xpos=self.xpos+1
    if self.xpos==self.width:
      self.xpos=self.xpos*3
      while self.xpos<self.width_bytes:
        self.out.write(str("%c" % 0))
        self.xpos=self.xpos+1
      self.xpos=0

  def dump(self):
    v = self.out.getvalue()
    self.out.close()
    return v
 
