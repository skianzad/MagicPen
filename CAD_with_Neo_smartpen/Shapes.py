'''
Created on 2020-02-11

@author: Guanxiong
'''

import math

class Circle():
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

class Rectangle():
    def __init__(self, upperleft_x, upperleft_y, center_x, center_y):
        self.upperleft_x = upperleft_x
        self.upperleft_y = upperleft_y
        self.center_x = center_x
        self.center_y = center_y

class Triangle():
    def __init__(self, x_0, y_0, x_1, y_1, x_2, y_2):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = x_1
        self.y_1 = y_1
        self.x_2 = x_2
        self.y_2 = y_2

class Line():
    def __Init__(self, x_0, y_0, x_1, y_1):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = x_1
        self.y_1 = y_1

class DistMeasurement():
    def __Init__(self):
        self.x_0 = 0
        self.y_0 = 0
        self.x_1 = 0
        self.y_1 = 0
        self.dist = 0

    def set_dist(self, x_0, y_0, x_1, y_1):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = x_1
        self.y_1 = y_1
        self.dist = math.sqrt(math.pow(self.x_0-self.x_1, 2) + math.pow(self.y_0-self.y_1, 2))
