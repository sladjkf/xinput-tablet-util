#!/usr/bin/python
from tkinter import *
from tkinter.ttk import *

from pynput import keyboard
from pynput import mouse

from Tablet import MyTablet
import GetDevDispl
class App():
    def __init__(self,master):
        frame = Frame(master)
        frame.pack()

        master.title("Tablet mapping utility")

        # Placeholder tablet object
        self.my_tablet = None
        # Drop down menu to select tablet device
        device_list = ["<none>"]
        with open("device_names") as devices:
            devices = devices.read().strip()
            device_list += devices.split("\n")
        self.current_device_name = StringVar(frame)
        self.current_device_name.set(device_list[0])
        self.current_device_name.trace("w",self.device_selected)

        self.opt_chooser = OptionMenu(frame,self.current_device_name, *device_list)
        # Buttons
        self.swap_button = Button(frame,text= "Swap", width=10)
        self.swap_button['command'] = self.swap

        self.map_button = Button(frame,text= "Map", width=10)
        self.map_button['command']=self.map
        # Labels
        self.map_label_text = StringVar(frame)
        self.map_label = Label(frame,textvariable=self.map_label_text)
        self.map_label_text.set("none")

        self.swap_label_text = StringVar(frame)
        self.swap_label = Label(frame,textvariable=self.swap_label_text)
        self.swap_label_text.set("none")

        # Place widgets on grid
        self.opt_chooser.grid(row=0,column=1)

        self.swap_button.grid(row=2,column=0)
        self.swap_label.grid(row=3,column=0)

        self.map_button.grid(row=2,column=2)
        self.map_label.grid(row=3,column=2)

    '''
    Callback function for the option menu to select the tablet device.
    '''
    def device_selected(self,*args):
        my_device_name = self.current_device_name.get()

        if my_device_name == "<none>":
            return

        dev_and_displ = GetDevDispl.get_devices_and_displays()

        my_dev_id = dev_and_displ['devices'][my_device_name]
        print(dev_and_displ)
        self.my_tablet = MyTablet(my_dev_id, dev_and_displ['displays'])
    def swap(self):
        if self.my_tablet == None:
            return

        self.my_tablet.swap()
        self.swap_label_text.set(self.my_tablet.displays[self.my_tablet.current_mapping])
    '''
    Function that runs the process of mapping the tablet to a limited touch area on screen.
    Press ALT on the corners of that touch area to map it.
    '''
    def map(self):
        if self.my_tablet == None:
            return

        event_queue = []

        def on_press(key):
            event_queue.append((key,"press"))

        def on_release(key):
            event_queue.append((key,"release"))

        class XYChosen(Exception): pass

        #----------------------
        mouse_data_controller = mouse.Controller()
        keyboard_data_controller = keyboard.Controller()

        mouse_listener = mouse.Listener()
        keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

        mouse_listener.start()
        keyboard_listener.start()

        #position pair 1: top left corner of active area
        x1y1 = ()
        #position pair 2: bottom right corner of active area
        x2y2 = ()

        #track button state (on the second button press end the loop)
        times_alt_pressed = 0

        while True:
            try:
                #debugging
                print(mouse_data_controller.position)
                print((x1y1,x2y2))
                print(event_queue)

                for event in event_queue:
                    if event[0] == keyboard.Key.alt and times_alt_pressed == 0 and event[1] == "press": #on the first button press that's an alt
                        times_alt_pressed += 1 #increment times pressed
                        x1y1 = mouse_data_controller.position #update the tuple that describes the top left corner
                        continue
                    if event[0] == keyboard.Key.alt and times_alt_pressed == 1 and event[1] == "press": #on the 2nd button press that's an alt
                        x2y2 = mouse_data_controller.position #update the tuple that describes the bottom right corner
                        raise XYChosen #end the loop
                try: #remove events from queue after processing. Enclosed in a try catch so IndexErrors don't cause the program to die immediately after starting
                    del event_queue[0]
                except IndexError:
                    pass
                #time.sleep(1)
            except XYChosen: #end the loop
                break
            except KeyboardInterrupt: #stop on KeyboardInterrupt
                mouse_listener.stop()
                keyboard_listener.stop()
                break
        #stop the listeners
        mouse_listener.stop()
        keyboard_listener.stop()
        #print the recorded corner values
        print((x1y1,x2y2))

        #dimensions of the touch region (x,y)
        region_size = [abs(x1y1[0]-x2y2[0]) , abs(x1y1[1]-x2y2[1])] #differences of the corners

        #creating a region offset -needed to run the xsetwacom command
        region_offset = []
        #find the smaller x value and use that as the x offset
        region_offset.append(min([x1y1[0],x2y2[0]]))
        #find the smaller y value and use that as the y offset
        region_offset.append(min([x1y1[1],x2y2[1]]))

        print("-------------------") #debugging
        print(region_size)
        print(region_offset)

        self.map_label_text.set(str(region_size[0]) + "x" + str(region_size[1]) + "+" + str(region_offset[0]) + "," + str(region_offset[1]))
        self.my_tablet.restrict_range(region_size[0], region_size[1], region_offset[0],region_offset[1])


root = Tk()
root.style = Style()
root.style.theme_use("alt")

app = App(root)
root.mainloop()
