'''
Created on 2020-04-28

@author: Guanxiong
'''

import math
from Shapes import *

class Point():
    def __init__(self, x, y, belongObject):
        self.x = x
        self.y = y
        self.belongObject = belongObject

class Alignment():
    # max separations for alignment
    MAX_X_SEP = 10
    MAX_Y_SEP = 10

    def __init__(self):
        self.delta_x = 0
        self.delta_y = 0
        self.init_x = 0 # keeps old x and y for auxiliary lines
        self.init_y = 0

    # reset current object's center coordinates based on proximity to centers/corners of previous objects;
    # choose center x/y for min separation in x/y direction from previous object(s)
    def align_center(self, currObject, circList, rectList):
        # first record old x and y
        self.init_x = currObject.center_x
        self.init_y = currObject.center_y
        # identify all points within alignment range (MAX_X_SEP x MAX_X_SEP box)
        pt_list_x = []
        pt_list_y = []
        box_x_min = currObject.center_x - Alignment.MAX_X_SEP
        box_x_max = currObject.center_x + Alignment.MAX_X_SEP
        box_y_min = currObject.center_y - Alignment.MAX_Y_SEP
        box_y_max = currObject.center_y + Alignment.MAX_Y_SEP
        if box_x_min < 0:
            box_x_min = 0
        if box_y_min < 0:
            box_y_min = 0
        
        # choose closest on x dir
        for circle in circList:
            if circle.center_x >= box_x_min and circle.center_x <= box_x_max:
                pt = Point(circle.center_x, circle.center_y, circle)
                pt_list_x.append(pt)
        
        for rectangle in rectList:
            if rectangle.center_x >= box_x_min and rectangle.center_x <= box_x_max:
                pt = Point(rectangle.center_x, rectangle.center_y, rectangle)
                pt_list_x.append(pt)
            if rectangle.upperleft_x >= box_x_min and rectangle.upperleft_x <= box_x_max:
                pt = Point(rectangle.upperleft_x, rectangle.upperleft_y, rectangle)
                pt_list_x.append(pt)
            rect_ur_x, rect_ur_y = rectangle.get_upper_right()
            if rect_ur_x >= box_x_min and rect_ur_x <= box_x_max:
                pt = Point(rect_ur_x, rect_ur_y, rectangle)
                pt_list_x.append(pt)
            rect_ll_x, rect_ll_y = rectangle.get_lower_left()
            if rect_ll_x >= box_x_min and rect_ll_x <= box_x_max:
                pt = Point(rect_ll_x, rect_ll_y, rectangle)
                pt_list_x.append(pt)
            rect_lr_x, rect_lr_y = rectangle.get_lower_right()
            if rect_lr_x >= box_x_min and rect_lr_x <= box_x_max:
                pt = Point(rect_lr_x, rect_lr_y, rectangle)
                pt_list_x.append(pt)
        
        # choose closest on y dir
        for circle in circList:
            if circle.center_y >= box_y_min and circle.center_y <= box_y_max:
                pt = Point(circle.center_x, circle.center_y, circle)
                pt_list_y.append(pt)
        
        for rectangle in rectList:
            if rectangle.center_y >= box_y_min and rectangle.center_y <= box_y_max:
                pt = Point(rectangle.center_x, rectangle.center_y, rectangle)
                pt_list_y.append(pt)
            if rectangle.upperleft_y >= box_y_min and rectangle.upperleft_y <= box_y_max:
                pt = Point(rectangle.upperleft_x, rectangle.upperleft_y, rectangle)
                pt_list_y.append(pt)
            rect_ur_x, rect_ur_y = rectangle.get_upper_right()
            if rect_ur_y >= box_y_min and rect_ur_y <= box_y_max:
                pt = Point(rect_ur_x, rect_ur_y, rectangle)
                pt_list_y.append(pt)
            rect_ll_x, rect_ll_y = rectangle.get_lower_left()
            if rect_ll_y >= box_y_min and rect_ll_y <= box_y_max:
                pt = Point(rect_ll_x, rect_ll_y, rectangle)
                pt_list_y.append(pt)
            rect_lr_x, rect_lr_y = rectangle.get_lower_right()
            if rect_lr_y >= box_y_min and rect_lr_y <= box_y_max:
                pt = Point(rect_lr_x, rect_lr_y, rectangle)
                pt_list_y.append(pt)

        # decide if align with none or one or two
        if len(pt_list_x) == 0 and len(pt_list_y) == 0: # no alignment needed
            pass
        elif len(pt_list_x) == 0: # align on y then
            print("align on y only")
            pt_chosen = None
            self.delta_y = Alignment.MAX_Y_SEP
            for pt in pt_list_y:
                delta_y = abs(pt.y - currObject.center_y)
                if delta_y <= self.delta_y:
                    self.delta_y = delta_y
                    pt_chosen = pt
            currObject.center_y = pt_chosen.y     
        elif len(pt_list_y) == 0: # align on x then
            print("align on x only")
            pt_chosen = None
            self.delta_x = Alignment.MAX_X_SEP
            for pt in pt_list_x:
                delta_x = abs(pt.x - currObject.center_x)
                if delta_x <= self.delta_x:
                    self.delta_x = delta_x
                    pt_chosen = pt
            currObject.center_x = pt_chosen.x
        else:   # may align on both x and y
            pt_pairs = [] # find pair of points belonging to different objects
            for pt_in_range_x in pt_list_x:
                for pt_in_range_y in pt_list_y:
                    if pt_in_range_y.belongObject is not pt_in_range_x.belongObject:
                        pt_pairs.append((pt_in_range_x, pt_in_range_y))
            if len(pt_pairs) == 0: # if no pairs found then no alignment
                pass
            else:
                print("align both")
                pt_pair_chosen = pt_pairs[0] # for now, choosen the 1st one
                self.delta_x = abs(pt_pair_chosen[0].x - currObject.center_x)
                self.delta_y = abs(pt_pair_chosen[1].y - currObject.center_y)
                currObject.center_x = pt_pair_chosen[0].x
                currObject.center_y = pt_pair_chosen[1].y
            
    
    # reset a rectangle's UL coordinates based on proximity to centers/corners of previous objects;
    # choose corner x/y for min separation in x/y direction from previous object(s)
    # require current object being a rectangle
    def align_corner(self, currObject, circList, rectList):
        # first record old x and y
        self.init_x = currObject.upperleft_x
        self.init_y = currObject.upperleft_y

        # identify all points within alignment range (MAX_X_SEP x MAX_X_SEP box)
        pt_list_x = []
        pt_list_y = []
        box_x_min = currObject.upperleft_x - Alignment.MAX_X_SEP
        box_x_max = currObject.upperleft_x + Alignment.MAX_X_SEP
        box_y_min = currObject.upperleft_y - Alignment.MAX_Y_SEP
        box_y_max = currObject.upperleft_y + Alignment.MAX_Y_SEP
        if box_x_min < 0:
            box_x_min = 0
        if box_y_min < 0:
            box_y_min = 0
        
        # choose closest on x dir
        for circle in circList:
            if circle.center_x >= box_x_min and circle.center_x <= box_x_max:
                pt = Point(circle.center_x, circle.center_y, circle)
                pt_list_x.append(pt)
        
        for rectangle in rectList:
            if rectangle.center_x >= box_x_min and rectangle.center_x <= box_x_max:
                pt = Point(rectangle.center_x, rectangle.center_y, rectangle)
                pt_list_x.append(pt)
            if rectangle.upperleft_x >= box_x_min and rectangle.upperleft_x <= box_x_max:
                pt = Point(rectangle.upperleft_x, rectangle.upperleft_y, rectangle)
                pt_list_x.append(pt)
            rect_ur_x, rect_ur_y = rectangle.get_upper_right()
            if rect_ur_x >= box_x_min and rect_ur_x <= box_x_max:
                pt = Point(rect_ur_x, rect_ur_y, rectangle)
                pt_list_x.append(pt)
            rect_ll_x, rect_ll_y = rectangle.get_lower_left()
            if rect_ll_x >= box_x_min and rect_ll_x <= box_x_max:
                pt = Point(rect_ll_x, rect_ll_y, rectangle)
                pt_list_x.append(pt)
            rect_lr_x, rect_lr_y = rectangle.get_lower_right()
            if rect_lr_x >= box_x_min and rect_lr_x <= box_x_max:
                pt = Point(rect_lr_x, rect_lr_y, rectangle)
                pt_list_x.append(pt)
        
        # choose closest on y dir
        for circle in circList:
            if circle.center_y >= box_y_min and circle.center_y <= box_y_max:
                pt = Point(circle.center_x, circle.center_y, circle)
                pt_list_y.append(pt)
        
        for rectangle in rectList:
            if rectangle.center_y >= box_y_min and rectangle.center_y <= box_y_max:
                pt = Point(rectangle.center_x, rectangle.center_y, rectangle)
                pt_list_y.append(pt)
            if rectangle.upperleft_y >= box_y_min and rectangle.upperleft_y <= box_y_max:
                pt = Point(rectangle.upperleft_x, rectangle.upperleft_y, rectangle)
                pt_list_y.append(pt)
            rect_ur_x, rect_ur_y = rectangle.get_upper_right()
            if rect_ur_y >= box_y_min and rect_ur_y <= box_y_max:
                pt = Point(rect_ur_x, rect_ur_y, rectangle)
                pt_list_y.append(pt)
            rect_ll_x, rect_ll_y = rectangle.get_lower_left()
            if rect_ll_y >= box_y_min and rect_ll_y <= box_y_max:
                pt = Point(rect_ll_x, rect_ll_y, rectangle)
                pt_list_y.append(pt)
            rect_lr_x, rect_lr_y = rectangle.get_lower_right()
            if rect_lr_y >= box_y_min and rect_lr_y <= box_y_max:
                pt = Point(rect_lr_x, rect_lr_y, rectangle)
                pt_list_y.append(pt)

        # decide if align with none or one or two
        if len(pt_list_x) == 0 and len(pt_list_y) == 0: # no alignment needed
            pass
        elif len(pt_list_x) == 0: # align on y then
            print("align on y only")
            pt_chosen = None
            self.delta_y = Alignment.MAX_Y_SEP
            for pt in pt_list_y:
                delta_y = abs(pt.y - currObject.upperleft_y)
                if delta_y <= self.delta_y:
                    self.delta_y = delta_y
                    pt_chosen = pt
            currObject.upperleft_y = pt_chosen.y     
        elif len(pt_list_y) == 0: # align on x then
            print("align on x only")
            pt_chosen = None
            self.delta_x = Alignment.MAX_X_SEP
            for pt in pt_list_x:
                delta_x = abs(pt.x - currObject.upperleft_x)
                if delta_x <= self.delta_x:
                    self.delta_x = delta_x
                    pt_chosen = pt
            currObject.upperleft_x = pt_chosen.x
        else:   # may align on both x and y
            pt_pairs = [] # find pair of points belonging to different objects
            for pt_in_range_x in pt_list_x:
                for pt_in_range_y in pt_list_y:
                    if pt_in_range_y.belongObject is not pt_in_range_x.belongObject:
                        pt_pairs.append((pt_in_range_x, pt_in_range_y))
            if len(pt_pairs) == 0: # if no pairs found then no alignment
                pass
            else:
                print("align both")
                pt_pair_chosen = pt_pairs[0] # for now, choosen the 1st one
                self.delta_x = abs(pt_pair_chosen[0].x - currObject.upperleft_x)
                self.delta_y = abs(pt_pair_chosen[1].y - currObject.upperleft_y)
                currObject.upperleft_x = pt_pair_chosen[0].x
                currObject.upperleft_y = pt_pair_chosen[1].y

class Distance():
    def __init__(self):
        self.delta_x = 0
        self.delta_y = 0
        self.init_x = 0 # keeps old x and y for auxiliary lines
        self.init_y = 0

    # Reset current object's center coordinates so the center is at the specified
    # distance from the last object;
    # Require at least one distance measurement;
    # Require current & last object being circle/rectangle
    def fix_distance(self, currObject, lastObject, distMeasurementList):
        if (isinstance(currObject, Circle) is False) and (isinstance(currObject, Rectangle) is False):
            print("need the current object being a rectangle or a circle")
            return
        if (isinstance(lastObject, Circle) is False) and (isinstance(lastObject, Rectangle) is False):
            print("need the last object being a rectangle or a circle")
            return
        
        current_x = currObject.center_x
        current_y = currObject.center_y
        last_x = lastObject.center_x
        last_y = lastObject.center_y
        assert len(distMeasurementList)>=1
        dist = distMeasurementList[len(distMeasurementList)-1].dist

        slope = (current_y - last_y) / (current_x - last_x)
        dx = math.sqrt(math.pow(dist,2) / (1 + math.pow(slope, 2)))
        if (current_x - last_x) < 0:
            dx = -1 * dx
        dy = slope * dx
        
        currObject.center_x = last_x + dx
        currObject.center_y = last_y + dy

        self.init_x = current_x
        self.init_y = current_y
        self.delta_x = abs(dx)
        self.delta_y = abs(dy)

class Concentric():
    # max separation radius for center coordinates
    MAX_SEP = 10

    def __init__(self):
        self.delta_x = 0
        self.delta_y = 0
        self.init_x = 0 # keeps old x and y for auxiliary lines
        self.init_y = 0
    
    # make current circle concentric with previous circles
    def make_concentric(self, currObject, circList):
        # check if current object is circle
        if isinstance(currObject, Circle) is False:
            print("need the current object being a circle")
            return

        # first record old x and y
        self.init_x = currObject.center_x
        self.init_y = currObject.center_y
        
        # identify closest center within alignment range (circular region with radius MAX_SEP)
        chosen_center_x = 0
        chosen_center_y = 0
        min_dist_squared = math.pow(Concentric.MAX_SEP, 2) + math.pow(Concentric.MAX_SEP, 2)
        for circle in circList:
            dx = currObject.center_x - circle.center_x
            dy = currObject.center_y - circle.center_y
            dist_squared = math.pow(dx, 2) + math.pow(dy, 2)
            if dist_squared <= min_dist_squared:
                min_dist_squared = dist_squared
                chosen_center_x = circle.center_x
                chosen_center_y = circle.center_y
        currObject.center_x = chosen_center_x
        currObject.center_y = chosen_center_y
        self.delta_x = abs(currObject.center_x - self.init_x)
        self.delta_y = abs(currObject.center_y - self.init_y)


