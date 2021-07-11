#!/usr/bin/env python3
import subprocess
import time
import re
import json

#figure out what command it is and execute
def is_command(command):
	#stop server and python script
	print("finding what command was stated")
	if command == "~stop":
		f.truncate(0)
		subprocess.run('./stop.sh', shell=True)
	#restart server from previous save
	elif command == "~back":
		pass
	#delete saves and make a new map
	elif command == "~reset":
		#stop factorio
		subprocess.run('pkill factorio',shell=True)
		#remove previous saves
		try:
			subprocess.run('rm saves/*',shell=True)
		except:
			print("no saves yet")
		#make map
		subprocess.run('./new_map.sh',shell=True)
		#run map
		subprocess.run('bin/x64/factorio --start-server-load-latest --server-settings data/server-settings.json --server-adminlist server-adminlist.json --console-log log.txt',shell=True)
#is an admin saying a command?
def find_command(line):
	for admin in admin_list:
		for command in command_list:
			print("searching for {} saying {}".format(admin, command))
			#this pattern will match a command said by an admin
			pattern = r"^\d+-\d+-\d+\s\d+:\d+:\d+\s\[CHAT\].*"+re.escape(admin)+r":.*"+re.escape(command)+r"$"
			match = re.search(pattern, line)
			if match != None:
				is_command(command)



#kill process in bash
#pgrep ./log_file_parser.py -f | xargs -r kill


#run script
#subprocess.run('./practice.sh', shell=True)

#sleep code
#time.sleep(3)

admin_list = []
command_list = ["~reset", "~back", "~stop"]

while True:
	time.sleep(10)
	#get current admin list
	with open('server-adminlist.json',"r") as j:
		data = json.load(j)
		admin_list = data
	#see if there are commands in log file
	with open('log.txt',"r+") as f:
		for line in f:
			find_command(line)
	#clear file
		print("clearing file")
		f.truncate(0)