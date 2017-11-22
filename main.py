import os

from utils.properties import Properties
import shutil
import subprocess


def is_same_file_name(file_name , name_list):
	for name in name_list:
		if file_name == name:
			return True
	return False


property = Properties("config.properties").getProperties()

source_dir_path = property['source']['dir']['path']
target_dir_path = property['target']['dir']['path']

target_run_command = property['target']['run']['command']

target_debug_info_command = property['target']['debug']['info']['command']

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

subprocess.call(target_run_command, shell=True)
subprocess.call(target_debug_info_command, shell=True)

