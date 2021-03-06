#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 19:21:27 2017

@author: cadmium
"""

import glob
import os


import cv2
import numpy as np

import tortoise as t



eye = t.peripheral.eye


class Routing(t.Task):
    def __init__(self):
        super(Routing, self).__init__()

        self.model = cv2.ml.ANN_MLP_load('E:/TDPS/data_0412/train/mlp28_0.003_0.0_0.5.xml')
		self.result = []
		self.count_curve = 0
		self.average_length = 30

    def step(self):
        img = eye.see()
        img_convert = Converting(img)
        image_array = Img_reshape(img_convert)
        ret, resp = self.model.predict(image_array)
        prediction = resp.argmax(-1)
        l, r =Direction_define(prediction)
        t.peripheral.wheels.set_lr(l, r)
		self.results, self.count_curve = Task_alter(prediction,self.results,self.count_curve,self.average_length)
        

        
def Task_alter(prediction,results,count_curve,average_length):
	results_length = len(results)
	
	if results_length < average_length:
		results.append(prdiction)
	else:
		results = Left_shift(prediction,results)
		results, count_curve = Judge_average(results,count_curve)
		
	return results, count_curve

def Left_shift(prediction,results):
	results = results.pop(0)
	results.append(prediction)
	return results

def Judge_average(results,count_curve):
	results_average = sum(results)/len(results)
	if results_average > 3.9 or results_average < 0.1:
		count_curve += 1
		results = []
		return results, count_curve
	else:
		return results, count_curve
	
	
	
def Converting(pic):
    im = Load_img(pic, ratio=0.5)
    v = im[:,:,2]
    dx, dy = np.gradient(v)
    g = (dx**2 + dy**2)**0.6
    g = g/g.max()*255
    
    core1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    g = cv2.erode(g, core1)
    g = g.astype(dtype=np.uint8)
    g = cv2.equalizeHist(g)
    core2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    g = cv2.erode(g, core2)
    
    g = g[120:240,:]
      
    return g

def Load_img(pic, ratio=0.5):
    im = pic

    h,w = im.shape[0:2]

    im = cv2.resize(im, dsize=(int(w*ratio), int(h*ratio)))

    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    
       
    return im

def Img_reshape(pic):
    im = pic.reshape(1, 44800).astype(np.float32)
    return im

def Direction_define(prediction):
    direction = prediction[0]
    if direction == 0:
        return 1, 0.2
    elif direction == 1:
        return 1, 0.7
    elif direction == 2:
        return 0.5, 0.5
    elif direction == 3:
        return 0.7, 1
    elif direction == 4:
        return 0.4, 1




if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = Routing()
    tttt.walk()