import os

from utils.properties import Properties
import shutil
import subprocess
import time
import sys

def is_same_file_name(file_name , name_list):
	for name in name_list:
		if file_name == name:
			return True
	return False

def exec_shell_command(command):
	print command
	subprocess.call(command, shell=True)

def back_up(source_path,target_path):

	if source_path is None or "" == source_path:
		return

	index = source_path.rfind('/')
	if index == -1:
		return

	length = len(source_path)
	dir_name = source_path[index+1:length]

	time_str = time.strftime("%Y%m%d_%H:%M:%S", time.localtime())

	back_up_file_name = dir_name + "_" + time_str + ".zip"

	command = 'zip -r ' + target_path  + "/" + back_up_file_name + " " + source_path
	print command

	exec_shell_command(command)


def unzip(source_file_path , target_path):
	unzip_command = "unzip "  + source_file_path + " -d " + target_path
	exec_shell_command(unzip_command)


def del_dir(dir_path):
	command = "rm -rf " + dir_path
	exec_shell_command(command)

property = Properties( sys.path[0] + "/config.properties").getProperties()

source_dir_path = property['source']['dir']['path']
target_dir_path = property['target']['dir']['path']
target_run_command = property['target']['run']['command']
unzip_file_path = property['unzip']['file']['path']
target_debug_info_command = property['target']['debug']['info']['command']
back_up_dir = property['bakup']['dir']['path']

back_up(target_dir_path,back_up_dir)

del_dir(target_dir_path)

unzip(unzip_file_path,target_dir_path)

source_file_name_list = os.listdir(source_dir_path)

for root, dirs, files in os.walk(target_dir_path):
	for file_name in files:

		if is_same_file_name(file_name,source_file_name_list) :
			target_path = os.path.join(root, file_name)

			source_file_path = source_dir_path + "/" + file_name
			shutil.copyfile(source_file_path ,target_path)

			print "-------------------------"
			print target_path
			print "-------------------------"

exec_shell_command(target_run_command)
exec_shell_command(target_debug_info_command)

