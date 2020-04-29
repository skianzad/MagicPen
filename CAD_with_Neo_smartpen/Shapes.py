'''
Created on 2020-02-11

@author: Guanxiong
'''

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
    def __Init__(self, x_0, y_0, x_1, y_1):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_1 = x_1
        self.y_1 = y_1

class DistMeasurement():
    def __Init__(self):
        self.dist = 0

    def set_dist(self, dist):
        self.dist = dist