import os, sys, array, random, time, string, pickle

from os import path
from time import sleep
from datetime import datetime
import logging

import seqarchtool_config as cfg



def logging_bucket(messages):
	logging.basicConfig(filename='seqarchtool.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
	logging.info('%s', messages)
	print(str(datetime.now())+messages)
    # logging_bucket(" >> Window opening..")	



