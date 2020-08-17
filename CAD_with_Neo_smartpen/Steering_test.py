# -*- coding: utf-8 -*-
'''
Created on 2020-08-16

Unit tests for the Steering module

@author: Guanxiong
'''

from Shapes import *
from Steering import Steering
import math

ID = 14.4
steering = Steering(ID)

def test_circle():
    c_x = 300
    c_y = 300
    r = 120
    circ = Circle(c_x, c_y, r)

    # case where the point is out of boundary by y
    pt_x = 300
    pt_y = 385
    if steering.is_in_tunnel(pt_x, pt_y, circ) is True:
        print("failed test_circle: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is out of boundary by x
    pt_x = 450
    pt_y = 300
    if steering.is_in_tunnel(pt_x, pt_y, circ) is True:
        print("failed test_circle: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is inside boundary
    pt_x = 425
    pt_y = 301
    if steering.is_in_tunnel(pt_x, pt_y, circ) is False:
        print("failed test_circle: x = " + str(pt_x) + " y = " + str(pt_y))

def test_rectangle():
    c_x = 500
    c_y = 500
    ul_x = 380
    ul_y = 440
    rect = Rectangle(ul_x, ul_y, c_x, c_y)
        
    # case where the point is inside region 1
    pt_x = 385
    pt_y = 500
    if steering.is_in_tunnel(pt_x, pt_y, rect) is False:
        print("failed test_rectangle: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is inside region 2
    pt_x = 500
    pt_y = 442
    if steering.is_in_tunnel(pt_x, pt_y, rect) is False:
        print("failed test_rectangle: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is inside region 3
    pt_x = 600
    pt_y = 500
    if steering.is_in_tunnel(pt_x, pt_y, rect) is False:
        print("failed test_rectangle: x = " + str(pt_x) + " y = " + str(pt_y))

    # case where the point is inside region 4
    pt_x = 500
    pt_y = 555
    if steering.is_in_tunnel(pt_x, pt_y, rect) is False:
        print("failed test_rectangle: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is outside boundary
    pt_x = 330
    pt_y = 480
    if steering.is_in_tunnel(pt_x, pt_y, rect) is True:
        print("failed test_rectangle: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is outside boundary
    pt_x = 650
    pt_y = 440
    if steering.is_in_tunnel(pt_x, pt_y, rect) is True:
        print("failed test_rectangle: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is outside boundary
    pt_x = 580
    pt_y = 530
    if steering.is_in_tunnel(pt_x, pt_y, rect) is True:
        print("failed test_rectangle: x = " + str(pt_x) + " y = " + str(pt_y))


def test_line():
    x_0 = 50
    y_0 = 50
    x_1 = 330
    y_1 = 50
    line = Line(x_0, y_0, x_1, y_1)

    # case where the point is out of boundary, horizontal line
    pt_x = 110
    pt_y = 71
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with horizontal line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is out of boundary, horizontal line
    pt_x = 110
    pt_y = 29
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with horizontal line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is out of boundary, horizontal line
    pt_x = 27
    pt_y = 50
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with horizontal line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is out of boundary, horizontal line
    pt_x = 352
    pt_y = 50
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with horizontal line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is inside boundary, horizontal line
    pt_x = 332
    pt_y = 52
    if steering.is_in_tunnel(pt_x, pt_y, line) is False:
        print("failed test_line with horizontal line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    x_0 = 100
    y_0 = 20
    x_1 = 100
    y_1 = 300
    line = Line(x_0, y_0, x_1, y_1)

    # case where the point is out of boundary, vertical line
    pt_x = 77
    pt_y = 90
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with vertical line: x = " + str(pt_x) + " y = " + str(pt_y))

    # case where the point is out of boundary, vertical line
    pt_x = 122
    pt_y = 90
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with vertical line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is out of boundary, vertical line
    pt_x = 100
    pt_y = 2
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with vertical line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is out of boundary, vertical line
    pt_x = 100
    pt_y = 311
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with vertical line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is inside boundary, vertical line
    pt_x = 100.2
    pt_y = 200
    if steering.is_in_tunnel(pt_x, pt_y, line) is False:
        print("failed test_line with vertical line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    x_0 = 100
    y_0 = 100
    x_1 = 300
    y_1 = 200
    line = Line(x_0, y_0, x_1, y_1)
    tunnelWidthHalf = math.sqrt(5) * 100 / ID / 2

    # case where the point is out of boundary, regular line
    pt_x = 200
    pt_y = float(pt_x)/2 + 50 + (tunnelWidthHalf+1)*math.sqrt(5)/2
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with regular line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is out of boundary, regular line
    pt_x = 200
    pt_y = float(pt_x)/2 + 50 - (tunnelWidthHalf+1)*math.sqrt(5)/2
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with regular line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is out of boundary, regular line
    pt_x = 400
    pt_y = float(pt_x)/2 + 50
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with regular line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is out of boundary, regular line
    pt_x = 5
    pt_y = float(pt_x)/2 + 50
    if steering.is_in_tunnel(pt_x, pt_y, line) is True:
        print("failed test_line with regular line: x = " + str(pt_x) + " y = " + str(pt_y))
    
    # case where the point is inside of boundary, regular line
    pt_x = 200
    pt_y = float(pt_x)/2 + 50 - (tunnelWidthHalf-1)*math.sqrt(5)/2
    if steering.is_in_tunnel(pt_x, pt_y, line) is False:
        print("failed test_line with regular line: x = " + str(pt_x) + " y = " + str(pt_y))
    

test_circle()
test_rectangle()
test_line()
    