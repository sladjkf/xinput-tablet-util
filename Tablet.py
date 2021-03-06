import subprocess
import os
import GetDevDispl
from math import cos, sin, pi
import numpy as np
class MyTablet:
    '''
    Class intended to represent the tablet.
    Represent current mapping to a monitor as a property of object.
    Call method 'swap' to go to next listed monitor.
    '''

    def __init__(self, device_id, displays):
        '''
        device_id: int representing xinput id of device to map
        displays: a list of xrandr display names
        '''
        self.device_id = device_id
        self.displays = displays
        
        # current_mapping is the current display, represented as an index in self.displays.
        self.current_mapping = 0
        self.rotation = 0
        self.map()

    def map(self):
        '''
        Map the tablet object to the display identified by current_mapping.
        '''
        cmd = 'xinput' + ' map-to-output ' + str(self.device_id) + ' ' + self.displays[self.current_mapping]
        print(cmd)
        subprocess.call(cmd.split(' '))

    def swap(self):
        '''
        Increment the current screen mapping. Wraps around back to 0 otherwise.
        '''
        if self.current_mapping + 1 <= len(self.displays)-1:
            self.current_mapping += 1
            self.map()
        else:
            self.current_mapping = 0
            self.map()
    def get_screen_dimensions(self):
        '''
        Determines the dimensions of the bounding box that encloses the entire set of displays.
        Returns: (bb_width, bb_height) - the width and height of the bounding box.
        '''
        display_resolution_info = GetDevDispl.get_display_resolutions()
        print(display_resolution_info)
        screens = list(display_resolution_info.values())
        screens = [list(map(int,screen)) for screen in screens]
        print(screens) 
        # find the bounding box that just encloses the entire screen
        bb_width = 0
        bb_height = 0
        for screen in screens:
            bb_width = max(bb_width, screen[0]+screen[2])
            bb_height = max(bb_height, screen[1]+screen[3])

        return bb_width, bb_height
        
    def restrict_range(self,x_size,y_size,x_offset,y_offset):
        '''
        Calculates the values for the Coordinate Transformation Matrix and passes those values into xinput.
        x_size: int - describes the x_size of the region to bound the tablet in.
        y_size: int - describes the y_size of the region to bound the tablet in.
        x_offset, y_offset: int - describes how far from the origin the region should be located.
        Returns: Void function.
        '''
        SCREEN_WIDTH, SCREEN_HEIGHT = self.get_screen_dimensions()
        print("screen_dimensions:", SCREEN_WIDTH, SCREEN_HEIGHT)

        matrix_list = []
        matrix_list.append(x_size / SCREEN_WIDTH)
        matrix_list.append(0)
        matrix_list.append(x_offset / SCREEN_WIDTH)
        matrix_list.append(0)
        matrix_list.append(y_size / SCREEN_HEIGHT)
        matrix_list.append(y_offset / SCREEN_HEIGHT)
        matrix_list += [0,0,1]

        # You can add a rotation to the transformation matrix by simply multiplying it with
        # a matrix that describes the next operation.
        # matrix_list = []
        # # Try swapping coordinate names to compensate for shift from rotation.
        # s_x = x_size / SCREEN_WIDTH
        # s_y = y_size / SCREEN_HEIGHT
        # t_x = (x_offset ) / SCREEN_WIDTH
        # t_y = y_offset / SCREEN_HEIGHT
        # theta = pi/2

        # matrix_list.append([s_x,0,t_x])
        # matrix_list.append([0,s_y,t_y])
        # matrix_list.append([0,0,1])

        # print(matrix_list)
        # mat = np.matrix(matrix_list)

        # # TODO: there needs to be some sort of shift here, but idk what it needs to be
        # x_shift = (x_offset + x_size)/SCREEN_WIDTH
        # rotation_matrix = np.matrix([
        #     [0,-1,1],
        #     [1,0,0],
        #     [0,0,1],
        #     ])
        # translate_matrix = np.matrix([
        #     [1,0,t_x],
        #     [0,1,t_y],
        #     [0,0,1],
        #     ])
        # mat = mat*rotation_matrix
        # matrix_list = mat.tolist()

        matrix_list = list(map(str,matrix_list))
        # matrix_list = [x.strip('[]') for x in matrix_list] 
        # print(matrix_list)
        cmd_list = ['xinput','set-prop',str(self.device_id),'--type=float', '"Coordinate Transformation Matrix"'] + matrix_list

        my_cmd = ""
        for item in cmd_list:
            my_cmd += item + " "

        print(my_cmd)
        #subprocess.call(my_cmd)
        os.system(my_cmd)
