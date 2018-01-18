# -*-coding:utf-8-*-

import time
import json
import math
import numpy as np


def get_trend(time_list, index, start_value, climax_value):
    rise_list = []
    fall_list = []
    if index == 1:
        rise_list.append([time_list[0], climax_value])
        # fall_list
        a = [[1,math.log(1)],[1,math.log(1+len(time_list)-index)]]
        a = np.array(a)
        b = [math.log(climax_value+1), math.log(start_value+1)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(1,len(time_list)-index+1):
            tmp_value = math.exp(np.dot([1, math.log(1+i)],x))-1
            fall_list.append([time_list[index+i-1], tmp_value])

    elif index == len(time_list)-1:
        a = [[1,1],[1,index]]
        a = np.array(a)
        b = [math.log(start_value+1), math.log(climax_value+1)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(index):
            tmp_value = math.exp(np.dot([1,1+i],x))-1
            rise_list.append([time_list[i], tmp_value])
        fall_list.append([time_list[-1], 0.5*climax_value])

    elif index == len(time_list):
        a = [[1,1],[1,index]]
        a = np.array(a)
        b = [math.log(start_value+1), math.log(climax_value+1)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(index):
            tmp_value = math.exp(np.dot([1,1+i],x))-1
            rise_list.append([time_list[i], tmp_value])

    elif index == 0:
        # fall_list
        a = [[1,math.log(1)],[1,math.log(1+len(time_list)-index)]]
        a = np.array(a)
        b = [math.log(start_value+1), math.log(1)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(1,len(time_list)-index+1):
            tmp_value = math.exp(np.dot([1, math.log(1+i)],x)) -1
            fall_list.append([time_list[index+i-1], tmp_value])


    else:
        a = [[1,1],[1,index]]
        a = np.array(a)
        b = [math.log(start_value+1), math.log(climax_value+1)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(index):
            tmp_value = math.exp(np.dot([1,1+i], x))-1
            rise_list.append([time_list[i], tmp_value])

        # fall_list
        a = [[1,math.log(1)],[1,math.log(1+len(time_list)-index)]]
        a = np.array(a)
        b = [math.log(climax_value+1), math.log(start_value+1)]
        b = np.array(b)
        x = np.linalg.solve(a,b)
        for i in range(1,len(time_list)-index+1):
            tmp_value = math.exp(np.dot([1, math.log(1+i)],x))-1
            fall_list.append([time_list[index+i-1], tmp_value])

    return rise_list, fall_list

if __name__ == "__main__":
    task_list()



