
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 19:21:27 2017
@author: cadmium
"""



import cv2
import numpy as np
from collections import deque

import tortoise as t
#import recording


#t.update_config(TORTOISE_WALK_PERIOD = 1)
eye = t.peripheral.eye



class Routing(t.Task):
    def __init__(self):
        super(Routing, self).__init__()

        self.model = cv2.ml.ANN_MLP_load('/home/pi/ftp/tortoise-mbed/Routing_test/new_add.xml')
#	     self.recorder = recording.RecordingTask()
	self.results = deque(maxlen = 80)
	self.count_curve = 0
	self.average_length = 80
		
    def step(self):
        img = eye.see()
        img_convert = Converting(img)
        image_array = Img_reshape(img_convert)
        ret, resp = self.model.predict(image_array)
        prediction = resp.argmax(-1)
	prediction = prediction[0]
        l, r = Direction_define(prediction)
        t.peripheral.wheels.set_lr(l,r)
	self.results, self.count_curve = Task_alter(prediction,self.results,self.count_curve,self.average_length)
#       self.recorder.step()
	#print prediction	

def Task_alter(prediction,results,count_curve,average_length):
	results.append(prediction)
	results_length = len(results)
	if results_length < average_length:
		results.append(prediction)
		return results, count_curve
	else:
		results.append(prediction)
		results_average = sum(results)/len(results)
		if results_average > 3.9:
			count_curve += 1
			results = []
			print count_curve
			return results, count_curve
		else:
			return results, count_curve


def Converting(pic):
    pic = pic[240:480, 80:560]
    pic = Resize_img(pic, ratio=0.5)
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
	
    h, s, v = pic[:,:,0],pic[:,:,1],pic[:,:,2]
    core2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    h = cv2.medianBlur(h, 9)
    _, h = cv2.threshold(h, 0, 255, cv2.THRESH_OTSU)
    h = cv2.morphologyEx(h, cv2.MORPH_OPEN, core2)
    h = 255-h
  

    s = cv2.equalizeHist(s)
    s = cv2.medianBlur(s, 9)
    _, s = cv2.threshold(s, 0, 255, cv2.THRESH_OTSU)
    s = cv2.morphologyEx(s, cv2.MORPH_OPEN, core2)

    ssss = h & s
      
    return ssss

def Resize_img(pic, ratio=0.5):
    h,w = pic.shape[0:2]

    pic = cv2.resize(pic, dsize=(int(w*ratio), int(h*ratio)))

              
    return pic

def Img_reshape(pic):
    im = pic.reshape(1, 28800).astype(np.float32)
    return im

def Direction_define(prediction):
    direction = prediction
    if direction == 0:
        return 0.125, 0.8
    elif direction == 1:
        return 0.2, 0.3
    elif direction == 2:
        return 0.34, 0.3
    elif direction == 3:
        return 0.3, 0.2
    elif direction == 4:
        return 0.75, 0.2




if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = Routing()
    tttt.walk()
