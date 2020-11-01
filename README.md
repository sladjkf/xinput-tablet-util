# xinput-tablet-util

A very hacky little program that will calculate a "Coordinate Transformation Matrix" for your graphics tablet (or xinput device) that you want to map to a limited region of your screen.

requires working:
- xinput
- xrandr
- pynput

Since the information is acquired by scraping the output from xinput, it's likely that the program won't work if xinput/xrandr have even slightly different outputs...

basic instructions:
- Run the xinput command and find your graphics tablet in the list.
- Place the name of your device exactly as it appears in a plaintext file called device\_names, in the same directory as the python files.
- Run ./main\_gui.py
	- Press Swap to cycle between different monitors.
	- Press Map to restrict your tablet to a certain area on your screen. 
		- Press Alt twice, once at the coordinates of your top left corner and once more at the coordinates of your bottom right corner.
		- The coordinates and offset of your region should appear in the GUI.
