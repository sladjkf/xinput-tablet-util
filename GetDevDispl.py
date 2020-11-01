import subprocess
import re
def get_devices_and_displays():
	devices = {}
	displays = []

	# get list of devices from xinput
	xinput_devs = str(subprocess.check_output(['xinput'])).strip()

	xinput_devs = xinput_devs.split('\\n')

	for device in xinput_devs:
		# get this iteration's device id

		thisdev_id = re.findall(r"id=[\w]+",device)
		# if line is empty just break
		if len(thisdev_id) == 0:
			break
		thisdev_id = int(thisdev_id[0].strip('id='))
		#print(thisdev_id)

		# strip junk special characters preceding human-readable device name
		junk_regex = r"([\\][\w]{3})|b'"
		junk_match = re.search(junk_regex,device)
		# stop loop if = \tid, because then all junk characters are stripped
		while junk_match != None and junk_match.group(0) != '\\tid':
			device = re.sub(junk_regex, '', device, count=1)
			#print(device)
			junk_match = re.search(junk_regex,device)

		# get this iteration's device name
		thisdev_name = device.split('\\t')[0].strip()

		# add it to the dictionary
		devices[thisdev_name] = thisdev_id

	# get list of displays from xrandr
	xrandr_displays = str(subprocess.check_output(['xrandr'])).strip()
	xrandr_displays = xrandr_displays.split('\\n')

	for line in xrandr_displays:
		if 'connected' in line and 'disconnected' not in line:
			end_index = line.find('connected')
			displays.append(line[0:end_index].strip())

	return {'devices':devices, 'displays':displays}
'''
Returns a dictionary of displays
keys are display names
values are lists of resolution info, first 2 elements are resolution, 2nd are offset values.
'''
def get_display_resolutions():
	displays = {}
	# get list of displays from xrandr
	xrandr_displays = str(subprocess.check_output(['xrandr'])).strip()
	xrandr_displays = xrandr_displays.split('\\n')

	for line in xrandr_displays:
		if 'connected' in line and 'disconnected' not in line:
			end_index = line.find('connected')
			display_name = line[0:end_index].strip()
			resolution_info = re.findall(r'[\d]+x[\d]+\+[\d]+\+[\d]+',line)
			resolution_info = re.split(r'x|\+', resolution_info[0])
			displays[display_name] = resolution_info

	return displays
