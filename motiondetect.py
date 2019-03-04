import numpy as np


class MotionDetect:
    def __init__(self, how_many_tries=3, min_final_move=800, max_final_move=3000):
        """
        Class' constructor

        :param how_many_tries:  how many measurements
        :param min_final_move:  final detection variable lower set value
        :param max_final_move:  final detection variable upper set value
        """
        self.how_many_tries = how_many_tries
        self.min_final_move = min_final_move
        self.max_final_move = max_final_move

    def isMotionDetect(self, data):
        """
        Motion detection method
        
        :param data: lista parametrow / list of parameters
        :return: 'True' if application detect movement, and 'False' if application is not detect movement
        """

        self.data = data
        if (len(data) == 0):
            print("list is empty")
            return False

        measurement = 40
        list = []
        treshold_weight = 1 # Weight in calculation variable of motion sensors from app
        drift_weight = 10 # Weight in calculation variable of drift (how many move in image)


        for y in range(0, self.how_many_tries - 1):
            number_of_elements = len(self.data[y][u'motion'][u'data'])
            if (number_of_elements-measurement < 0):
                print("Motion detected: 0")
                return False

            for x in range(0, number_of_elements):
                list.append(float(str(self.data[y][u'motion'][u'data'][x][1]).replace('[', '').replace(']', '')))

        number_of_list = len(list)
        print(number_of_list)
        average = np.mean(list)

        diff = 0
        for i in range(1, int(number_of_list / 2)):
            diff = diff + abs(
                list[number_of_list - i] - list[0 + i])
        diff = abs(diff) / number_of_list
        if (diff == 0): diff = 0.1

        summary = (average * treshold_weight + diff * drift_weight) / treshold_weight + drift_weight

        if ((summary > self.min_final_move) and (summary < self.max_final_move)):
            print("Motion detected: 1")
            return True
        else:
            print("Motion detected: 0")
            return False
