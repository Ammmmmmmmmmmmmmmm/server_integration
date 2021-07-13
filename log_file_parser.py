#!/usr/bin/env python3
import subprocess
import time
import re
import json
import os

def clean():
	with open('log.txt',"r+") as f:
			#clear file
			print("clearing file")
			f.truncate(0)

#figure out what command it is and execute
def is_command(command):
	#stop server and python script
	print("command listed above initiated")
	if command == "~stop":
		f.truncate(0)
		subprocess.run('./stop.sh', shell=True)
	#restart server from previous save
	elif command == "~back":
		#stop factorio
		if len(os.listdir(os.path.join(os.getcwd(),'saves'))) < 2:
			print("can't go back anymore")
		else:
			subprocess.run('pkill factorio',shell=True)
			time.sleep(3)
			current_save = os.listdir(os.path.join(os.getcwd(),'saves'))[0]
			try:
				subprocess.run('mkdir reverts', shell=True)
				subprocess.run('cp saves/server.zip reverts', shell=True)
				subprocess.run('rm saves/server.zip', shell=True)
			except:
				print("no saves yet")
			for save in os.listdir(os.path.join(os.getcwd(),'saves')):
				if os.path.getmtime(os.path.join(os.getcwd(),'saves',save)) > os.path.getmtime(os.path.join(os.getcwd(),'saves',current_save)):	
					current_save = save
			path = os.path.join(os.getcwd(),'saves',current_save)
			print('removing {}'.format(path))
			subprocess.run('rm {}'.format(path), shell=True)
			clean()
			print("is running")
			subprocess.run('./run.sh',shell=True)
	#delete saves and make a new map
	elif command == "~reset":
		print("reset initiated")
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
		clean()
		subprocess.run('./run.sh',shell=True)
	elif command == "~revert":
		try:
			subprocess.run('cp reverts/* saves', shell=True)
			subprocess.run('rm reverts/*', shell=True)
			subprocess.run('pkill factorio',shell=True)
			clean()
			subprocess.run('./run.sh',shell=True)
		except:
			print("no reverts yet")
			break



#is an admin saying a command?
def find_command(line):
	for admin in admin_list:
		for command in command_list:
			print("searching for {} saying {}".format(admin, command))
			#this pattern will match a command said by an admin
			pattern = r"^\d+-\d+-\d+\s\d+:\d+:\d+\s\[CHAT\].*"+re.escape(admin)+r":.*"+re.escape(command)+r"$"
			match = re.search(pattern, line,re.IGNORECASE)
			if match != None:
				is_command(command)



#kill process in bash
#pgrep ./log_file_parser.py -f | xargs -r kill


#run script
#subprocess.run('./practice.sh', shell=True)

#sleep code
#time.sleep(3)

admin_list = []
command_list = ["~reset", "~back", "~stop","~revert"]
#make sure to start with clean log file
with open('log.txt',"r+") as f:
	#clear file
	print("clearing file")
	f.truncate(0)

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