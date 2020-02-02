import os
import zipfile
import sys
import logging
import shutil
import time

from os import listdir, path
from os.path import isfile, join, isdir
from time import sleep
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



def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


if __name__ == "__main__":
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

	for dirname in directory_list(cfg.origin_path):
		join_fullpath_path=os.path.join(cfg.origin_path, dirname)
		join_fullpath_with_filename=os.path.join(cfg.origin_path, dirname+".zip")
		join_destination_fullpath_with_filename=os.path.join(cfg.destination_path, dirname+".zip")
		logging_bucket(" >> Archiving "+dirname+".")
		arch_tic=time.process_time()
		directory_zip(join_fullpath_path, join_fullpath_with_filename)
		arch_toc=time.process_time()
		# "{0:.2f}".format(a)
		arch_proctime=str("{0:.2f}".format(arch_toc-arch_tic))
		logging_bucket(" >> Archiving time : "+str(arch_proctime)+"s.")	
		logging_bucket(" >> Archived file size :"+file_size(join_fullpath_with_filename)+".")
		logging_bucket(" >> Moving "+dirname+".zip. ")
		move_tic=time.process_time()
		shutil.move(join_fullpath_with_filename, join_destination_fullpath_with_filename)
		move_toc=time.process_time()
		move_proctime=str("{0:.2f}".format(move_toc-move_tic))
		logging_bucket(" >> Archiving and Moving OK "+dirname+".")
		logging_bucket(" >> File trasfer time: "+str(move_proctime)+"s.")	

	logging_bucket(" >> Done Archiving.")