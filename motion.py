import urllib.request as urllib2
import json
from time import sleep, time
import cv2
import numpy as np
import os


class SensorException(Exception):
    def __init__(self, sensor):
        """
        Sensor's exception in case it's not switched on
        :param sensor: specific sensor
        """
        super().__init__("Error: Sensor {} is not switched on".format(sensor))


class Motion:
    def __init__(self, ip_add, port="8080", how_many_tries=3, interval=1):
        """
        Class' constructor
        :param ip_add: user ip address
        :param port: user port
        :param how_many_tries: how many measurements
        :param interval: time between measurement
        countOffline: amount of tries for offline checking
        """
        self.ip_address = ip_add
        self.port = port
        self.how_many_tries = how_many_tries
        self.interval = interval
        self.countOffline = 0

    def isAppWorking(self):
        """
        Verifies if the application is working
        :return: "True" if application is working, and "False" if application is not working
        """
        try:
            url = urllib2.urlopen("http://" + self.ip_address + ":" + self.port + "/sensors.json?sense=motion")
        except urllib2.URLError as err:
            self.countOffline = self.countOffline + 1;
            print("Message isAppWorking():", err.reason, " ", self.countOffline)
        else:
            data = json.load(url)
            self.countOffline = 0
            if len(data) == 0:
                raise SensorException('motion')

        if (self.countOffline > 2):
            print("Message isAppWorking(): Application is not working")
            return False
        else:
            return True

    def motionData(self):
        """
        Returns data from the sensor
        :return: "[data]" if application is working and data url exists, "[]" if data url does not exist
        """
        list = []
        try:
            for y in range(0, self.how_many_tries):
                url = urllib2.urlopen("http://" + self.ip_address + ":" + self.port + "/sensors.json?sense=motion")
                data = json.load(url)
                list.append(data)
                sleep(self.interval)
        except urllib2.URLError as err:
            pass

        return list

    def savePicture(self):
        """

        :return: "tmp_url" into temporary image if application is working and data url exists,
                and "" if data url does not exist
        """
        self._createFolder('./tmp_img/')
        tmp_url = ''
        try:
            url = "http://" + self.ip_address + ":" + self.port + "/shot.jpg"
            imgResp = urllib2.urlopen(url)
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            tmp_url = "./tmp_img/" + str(int(time())) + ".jpg"
            cv2.imwrite(tmp_url, img)
        except urllib2.URLError as err:
            pass

        return tmp_url

    def _createFolder(self, directory):
        """
        Creates folder for temporary images
        :param directory: temporary name of the folder
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory. ' + directory)
