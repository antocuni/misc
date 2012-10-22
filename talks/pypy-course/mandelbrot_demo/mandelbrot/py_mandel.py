#!/usr/bin/python

import cStringIO
from py_kohn_bmp import kohn_bmp

## PyMandel - Mandelbrots generated in Python
## Copyright 2007 - Michael Kohn
## mike@mikekohn.net - http://www.mikekohn.net/
## adapted by Antonio Cuni - 2010

# Changing the values below will change the resulting image

def mandelbrot(image_width, image_height):
    start_real=-2.00
    start_imag=-1.00
    end_real=1.00
    end_imag=1.00

    my_bmp=kohn_bmp(image_width,image_height,3)

    colors = [ [0,0,0], [255,0,0], [127,0,0], 
               [127,127,0], [0,127,0], [0,255,0],
               [0,255,0], [0,255,127], [0,127,127],
               [0,127,255], [0,0,255], [127,0,255],
               [127,0,255], [255,0,255], [255,0,127],
               [127,127,0], [255,0,0] ]

    inc_real=(end_real-start_real)/image_width
    inc_imag=(end_imag-start_imag)/image_height

    start=complex(start_real,start_imag)
    end=complex(end_real,end_imag)

    for y in range(image_height):
        for x in range(image_width):
            c=complex(start_real+(inc_real*x),start_imag+(inc_imag*y))
            z=complex(0,0)
            count=169

            while count>0:
                z=(z**2)+c
                if abs(z)>2: break
                count=count-1

            c=int(count/10)
            my_bmp.write_pixel(colors[c][0],colors[c][1],colors[c][2])

    return my_bmp.dump()

