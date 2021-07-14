#!/usr/bin/env python3

import subprocess
import time
import re
import json
import os


def clean():
	"""clean log file"""
	with open('log.txt',"r+") as f:
			#clear file
			f.truncate(0)


def find_command(line):
	"""Find if admin is saying a command"""
	for admin in admin_list:
		for command in command_list:
			pattern = r"^\d+-\d+-\d+\s\d+:\d+:\d+\s\[CHAT\].*"+re.escape(admin)+r":.*"+re.escape(command)+r"$"
			match = re.search(pattern, line,re.IGNORECASE)
			if match != None:
				is_command(command)


def is_command(command):
	"""Figure out what command it is and execute"""

	#stop server and python script
	if command == "~stop":
		clean()
		subprocess.run('./stop.sh', shell=True)

	#restart server from previous save by moving current save to revert folder
	elif command == "~back":	
		if len(os.listdir(os.path.join(os.getcwd(),'saves'))) < 2:
			pass
		else:
			subprocess.run('pkill factorio',shell=True)
			time.sleep(3)
			current_save = os.listdir(os.path.join(os.getcwd(),'saves'))[0]
			for save in os.listdir(os.path.join(os.getcwd(),'saves')):
				if os.path.getmtime(os.path.join(os.getcwd(),'saves',save)) > os.path.getmtime(os.path.join(os.getcwd(),'saves',current_save)):	
					current_save = save
			path = os.path.join(os.getcwd(),'saves',current_save)
			subprocess.run('cp {} reverts'.format(path), shell=True)
			subprocess.run('rm {}'.format(path), shell=True)
			subprocess.run('rm {}'.format(path), shell=True)
			clean()
			subprocess.run('./run.sh',shell=True)

	#delete saves and make a new map
	elif command == "~reset":
		subprocess.run('pkill factorio',shell=True)
		subprocess.run('rm saves/*',shell=True)
		subprocess.run('./new_map.sh',shell=True)
		clean()
		subprocess.run('./run.sh',shell=True)

	#revert back command and go back the the initial map
	elif command == "~revert":
		if os.listdir("reverts") == []:
			pass
		else:
			subprocess.run('cp reverts/* saves', shell=True)
			subprocess.run('rm reverts/*', shell=True)
			subprocess.run('pkill factorio',shell=True)
			clean()
			time.sleep(3)
			subprocess.run('./run.sh',shell=True)


#makes saves and reverts folder if not yet there 
if "saves" not in os.listdir(os.getcwd()):
	subprocess.run('mkdir saves', shell=True)
if "reverts" not in os.listdir(os.getcwd()):
	subprocess.run('mkdir reverts', shell=True)


admin_list = []
command_list = ["~reset", "~back", "~stop","~revert"]


#start parsing loop
clean()
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
		f.truncate(0)

