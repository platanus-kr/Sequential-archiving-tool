import os
import zipfile
import sys
import logging
import shutil

from os import listdir, path
from os.path import isfile, join, isdir
from time import sleep, time
from datetime import datetime

import sequarchtool_config as cfg

def logging_bucket(messages):
	logging.basicConfig(filename='sequarchtool.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
	logging.info('%s', messages)
	print(str(datetime.now())+messages)
    # logging_bucket(" >> Window opening..")	


def directory_list(path):
    res = [f for f in listdir(path) if isdir(path)]
    return res

def directory_zip(src_fullpath, dest_filename):
	with zipfile.ZipFile(dest_filename, 'w') as zip_:
		rootpath = src_fullpath
		for (paths, dir__, files) in os.walk(src_fullpath):
			for f in files:
				fullpath = os.path.join(paths, f)
				relpath = os.path.relpath(fullpath, rootpath)
				zip_.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
		zip_.close()


try:
	os.path.isdir(cfg.destination_path)
except:
	logging_bucket(" >> Not found destination path.")
	exit()

try:
	os.path.isdir(cfg.origin_path)
except:
	logging_bucket(" >> Not found origin path.")
	exit()


try:
	join_path_dsstore=os.path.join(cfg.origin_path,".DS_Store")
	os.remove(join_path_dsstore)
	logging_bucket(" >> .DS_Store removed.")
except:
	pass

now = datetime.now()
nowDatetime = now.strftime('%Y%m%d')
# print(directory_list(cfg.origin_path))

for dirname in directory_list(cfg.origin_path):
	join_fullpath_path=os.path.join(cfg.origin_path, dirname)
	join_fullpath_with_filename=os.path.join(cfg.origin_path, dirname+".zip")
	join_destination_fullpath_with_filename=os.path.join(cfg.destination_path, dirname+".zip")
	logging_bucket(" >> Archiving "+dirname+".")
	directory_zip(join_fullpath_path, join_fullpath_with_filename)
	logging_bucket(" >> Moving "+dirname+".zip. ")
	shutil.move(join_fullpath_with_filename, join_destination_fullpath_with_filename)
	logging_bucket(" >> Archiving and Moving OK "+dirname+".")

logging_bucket(" >> Done Archiving.")