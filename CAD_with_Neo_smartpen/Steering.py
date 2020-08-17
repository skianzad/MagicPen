# -*- coding: utf-8 -*-
'''
Created on 2020-08-11

@author: Guanxiong
'''

from Shapes import *
import math
import numpy as np

class Steering():

    def __init__(self, indexOfDiff):
        self.indexOfDiff = indexOfDiff
    
    def is_in_tunnel(self, x, y, obj):
        '''
        checks if given point (x, y) is in the tunnel of the given object
        x: x coord of pen tip
        y: y coord of pen tip
        obj: the shape that user is drawing (circle/rectangle/...)
        '''
        if isinstance(obj, Circle):
            tunnelWidthHalf = math.pi * obj.radius / self.indexOfDiff / 2
            sqr = pow((x - obj.center_x), 2) + pow((y - obj.center_y), 2)
            if (sqr >= pow((obj.radius - tunnelWidthHalf), 2)) is False or (sqr <= pow((obj.radius + tunnelWidthHalf), 2)) is False:
                return False
            else:
                return True
        elif isinstance(obj, Rectangle):
            tunnelWidthHalf = (2.0*(obj.center_x - obj.upperleft_x)+2.0*(obj.center_y-obj.upperleft_y)) / self.indexOfDiff
            upper_left = (obj.upperleft_x, obj.upperleft_y)
            upper_right = obj.get_upper_right()
            lower_left = obj.get_lower_left()
            lower_right = obj.get_lower_right()
            if (x>=upper_left[0]-tunnelWidthHalf) and (x<=upper_left[0]+tunnelWidthHalf) and (y>=upper_left[1]-tunnelWidthHalf) and (y<=lower_left[1]+tunnelWidthHalf):
                return True
            elif (x>=upper_left[0]-tunnelWidthHalf) and (x<=upper_right[0]+tunnelWidthHalf) and (y>=upper_left[1]-tunnelWidthHalf) and (y<=upper_right[1]+tunnelWidthHalf):
                return True
            elif (x>=upper_right[0]-tunnelWidthHalf) and (x<=upper_right[0]+tunnelWidthHalf) and (y>=upper_right[1]-tunnelWidthHalf) and (y<=lower_right[1]+tunnelWidthHalf):
                return True
            elif (x>=lower_left[0]-tunnelWidthHalf) and (x<=lower_right[0]+tunnelWidthHalf) and (y>=lower_left[1]-tunnelWidthHalf) and (y<=lower_left[1]+tunnelWidthHalf):
                return True
            else:
                return False
        elif isinstance(obj, Line):
            tunnelWidthHalf = obj.get_magnitude() / self.indexOfDiff / 2.0
            if (obj.x_0 == obj.x_1): # vertical line
                if (x>=obj.x_0-tunnelWidthHalf) and (x<=obj.x_0+tunnelWidthHalf) and (y>=min(obj.y_0, obj.y_1)-tunnelWidthHalf) and (y<=max(obj.y_0, obj.y_1)+tunnelWidthHalf):
                    return True
                else:
                    return False
            elif (obj.y_0 == obj.y_1): # horizontal line
                if (y>=obj.y_0-tunnelWidthHalf) and (y<=obj.y_0+tunnelWidthHalf) and (x>=min(obj.x_0, obj.x_1)-tunnelWidthHalf) and (x<=max(obj.x_0, obj.x_1)+tunnelWidthHalf):
                    return True
                else:
                    return False
            else:
                A, B, C = obj.get_line_equation()
                dist = abs(A*x+B*y+C)/math.sqrt(pow(A,2)+pow(B,2))
                k1 = -1 * A
                b1 = -1 * C
                k2 = -1*(1/k1)
                b2 = y - k2*x
                xIntersect = (b2-b1)/(k1-k2)
                yIntersect = k1*xIntersect+b1
                distPt0 = math.sqrt(pow(xIntersect-obj.x_0, 2)+pow(yIntersect-obj.y_0, 2))
                distPt1 = math.sqrt(pow(xIntersect-obj.x_1, 2)+pow(yIntersect-obj.y_1, 2))
                dist2 = min(distPt0, distPt1)
                if dist<=tunnelWidthHalf and ((x>=min(obj.x_0, obj.x_1) and x<=max(obj.x_0, obj.x_1))  or dist2<=tunnelWidthHalf):
                    return True
                else:
                    return False
        else:
            return False