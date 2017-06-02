
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 19:21:27 2017
@author: cadmium
"""



import cv2
import numpy as np


import tortoise as t
#import recording


#t.update_config(TORTOISE_WALK_PERIOD = 1)
eye = t.peripheral.eye



class Routing2_part2(t.Task):
    def __init__(self):
        super(Routing2_part2, self).__init__()

        self.model = cv2.ml.ANN_MLP_load('/home/pi/ftp/tortoise-mbed/Routing_test/cloudy.xml')


		
    def step(self):
        img = eye.see()
        img_convert = Converting(img)
        image_array = Img_reshape(img_convert)
        ret, resp = self.model.predict(image_array)
        prediction = resp.argmax(-1)
        l, r = Direction_define(prediction)
        t.peripheral.wheels.set_lr(l, r)

#       print prediction[0]	

        

def Converting(pic):
    
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
    pic = Resize_img(pic, ratio=0.5)
	
    v = pic[:,:,2]
    dx, dy = np.gradient(v)
    g = (dx**2 + dy**2)**0.6
    g = g/g.max()*255
    
    core1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    g = cv2.erode(g, core1)
    g = g.astype(dtype=np.uint8)
    g = cv2.equalizeHist(g)
    core2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    g = cv2.erode(g, core2)
#    g = Resize_img(g,ratio = 0.5)    
    
    g = g[120:240,20:300]
      
    return g

def Resize_img(pic, ratio=0.5):
    
    h,w = pic.shape[0:2]

    pic = cv2.resize(pic, dsize=(int(w*ratio), int(h*ratio)))

              
    return pic

def Img_reshape(pic):
    im = pic.reshape(1, 33600).astype(np.float32)
    return im

def Direction_define(prediction):
    direction = prediction[0]
    if direction == 0:
        return 0.25, 0.9
    elif direction == 1:
        return 0.2, 0.3
    elif direction == 2:
        return 0.34, 0.3
    elif direction == 3:
        return 0.3, 0.2
    elif direction == 4:
        return 0.9, 0.2




if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = Routing2_part2()
    tttt.walk()
