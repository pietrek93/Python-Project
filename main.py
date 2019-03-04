#!/usr/bin/python
import urllib.request as urllib2
import json, numpy as np
from decimal import Decimal
from time import sleep
import cv2
import os
import datetime

from motion import Motion
from motionDetect import MotionDetect
from detect import Detect

try:
    # >3.2
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

config = ConfigParser()

# get the path to config.ini
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

config.read(config_path)

# Connection
IP = config.get('connection', 'ip')
PORT = config.get('connection', 'port')

#options
tries = config.getint('options', 'how_many_tries')
interval = config.getint('options', 'interval')

#detection
min_final_move = config.getint('detection', 'min_final_move')
max_final_move = config.getint('detection', 'max_final_move')

#face
scale_factor = config.getfloat('face', 'scale_factor')
min_neighbors = config.getfloat('face', 'min_neighbors')







connection = Motion(IP, PORT, tries, interval)
motion = MotionDetect(tries, min_final_move, max_final_move)


while(connection.isAppWorking()):
    data = connection.motionData()
    isMotionDetected = motion.isMotionDetect(data)
    print(isMotionDetected)
    if(isMotionDetected):
        imgSource = connection.savePicture()
        face = Detect(imgSource, scale_factor)
        if os.path.isdir("./faces"):
            pass
        else:
            connection._createFolder("./faces")
        if os.path.isdir("./faces/" + datetime.date.today().strftime("%d.%m.%y")):
            pass
        else:
            connection._createFolder("./faces/" + datetime.date.today().strftime("%d.%m.%y"))

        if (face.face_detect() is not None):
            if(len(face.face_detect())):
                face.facecrop(face.face_detect())


