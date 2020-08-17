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
    
    def set_center(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
    
    def set_radius(self, radius):
        self.radius = radius

class Arc():
    def __init__(self, center_x, center_y, start_x, start_y, end_x, end_y):
        self.center_x = center_x
        self.center_y = center_y
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
    
    def set_center(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
    
    def set_start(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
    
    def set_end(self, end_x, end_y):
        self.end_x = end_x
        self.end_y = end_y

class Rectangle():
    def __init__(self, upperleft_x, upperleft_y, center_x, center_y):
        self.upperleft_x = upperleft_x
        self.upperleft_y = upperleft_y
        self.center_x = center_x
        self.center_y = center_y
    
    def set_center(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
    
    def set_upper_left_coord(self, upperleft_x, upperleft_y):
        self.upperleft_x = upperleft_x
        self.upperleft_y = upperleft_y
    
    def get_length(self):
        return 2 * (self.center_x - self.upperleft_x)
    
    def get_height(self):
        return 2 * (self.center_y - self.upperleft_y)

    def get_upper_right(self):
        length = self.get_length()
        return (self.upperleft_x + length), self.upperleft_y
        
    def get_lower_left(self):
        height = self.get_height()
        return self.upperleft_x, (self.upperleft_y + height)
    
    def get_lower_right(self):
        length = self.get_length()
        height = self.get_height()
        return (self.upperleft_x + length), (self.upperleft_y + height)

class Triangle():
    def __init__(self, x_0, y_0, x_1, y_1, x_2, y_2):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = x_1
        self.y_1 = y_1
        self.x_2 = x_2
        self.y_2 = y_2

class Line():
    def set_coords(self, x_0, y_0, x_1, y_1):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = x_1
        self.y_1 = y_1

    def __init__(self, x_0, y_0, x_1, y_1):
        self.set_coords(x_0, y_0, x_1, y_1)

    # returns magnitude of the vector formed by the line's two points
    def get_magnitude(self):
        diff_x_sqrd = math.pow((self.x_1 - self.x_0), 2)
        diff_y_sqrd = math.pow((self.y_1 - self.y_0), 2)
        sqrt = math.sqrt(diff_x_sqrd + diff_y_sqrd)
        return abs(sqrt)
    
    # returns signed magnitude of the cross product of the line's vector
    # with another line's vector
    def get_cross_product(self, line):
        a1 = self.x_1 - self.x_0
        a2 = self.y_1 - self.y_0
        b1 = line.x_1 - line.x_0
        b2 = line.y_1 - line.y_0
        return (a1 * b2 - a2 * b1)
    
    # returns signed magnitude of the dot product of the line's vector
    # with another line's vector
    def get_dot_product(self, line):
        a1 = self.x_1 - self.x_0
        a2 = self.y_1 - self.y_0
        b1 = line.x_1 - line.x_0
        b2 = line.y_1 - line.y_0
        return (a1 * b1 + a2 * b2)
    
    # for an equation of the line, in the form Ax + By + C = 0; returns (A, B, C)
    def get_line_equation(self):
        if self.x_1 - self.x_0 == 0:
            return (1, 0, -1 * self.x_1)
        else:
            k = float(self.y_1 - self.y_0) / float(self.x_1 - self.x_0)
            b = self.y_1 - k * self.x_1
            return (-1*k, 1, -1*b)

class DistMeasurement():
    def __Init__(self):
        self.dist = 0

    def set_dist(self, dist):
        self.dist = dist