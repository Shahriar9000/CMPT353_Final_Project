import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os
currentdir = os.getcwd()
walking = os.path.join(currentdir, 'filtered_data/walk')
upstairs = os.path.join(currentdir, 'filtered_data/upstairs')
downstairs = os.path.join(currentdir, 'filtered_data/downstairs')
# print (currentdir)
x = pd.DataFrame()

def get_subject_and_foot(filename):
    base  = os.path.basename(filename)
    base = base.split(".")
    subject = base[0].split('_')
    subject, foot, secs, file_number = subject[2], subject[1], subject[3], subject[4]

    return (subject, foot, secs, file_number)

def allData(dirname, action):
    global x
    for filename in os.listdir(dirname):
        # print(x)
        # print ("!!!!!!!!!!!!!!!!!!",filename)
        file = os.path.join(dirname, filename)
        data = pd.read_csv(file)
        # print (data)
        noise_filtered = data[["time","ax","ay","az"]].copy()
        noise_filtered['prev_time'] = noise_filtered['time'].shift(1)
        noise_filtered = noise_filtered.dropna()
        noise_filtered['del_t'] = noise_filtered['time'] - noise_filtered['prev_time']
        noise_filtered['vx'] = noise_filtered['ax']*noise_filtered['del_t']
        noise_filtered['vy'] = noise_filtered['ay']*noise_filtered['del_t']
        noise_filtered['vz'] = noise_filtered['az']*noise_filtered['del_t']
        noise_filtered['px'] = noise_filtered['vx']*noise_filtered['del_t']
        noise_filtered['py'] = noise_filtered['vy']*noise_filtered['del_t']
        noise_filtered['pz'] = noise_filtered['vz']*noise_filtered['del_t']

        speed = None
        if (action in ['walking', 'jogging', 'running']):
            subject, foot, secs, file_number = get_subject_and_foot(filename)
            speed = 19.5/float(secs) # m/s

        # print(noise_filtered)

        # noise_filtered = noise_filtered.drop(['ax', 'ay', 'az'], axis = 1).copy()
        noise_filtered = noise_filtered.drop(['time', 'prev_time', 'del_t'], axis = 1).copy()
        noise_filtered = noise_filtered.drop(noise_filtered.index[0])

        noise_filtered = noise_filtered.values.flatten()
        noise_filtered = pd.DataFrame(noise_filtered).transpose()
        action_col = pd.DataFrame([[action, speed]], columns=['action', 'speed'])
        noise_filtered = pd.concat([action_col, noise_filtered], axis=1)
        # print(noise_filtered.shape)
        x = x.append(noise_filtered)


def createMlData():
    allData(walking, 'walking')
    allData(upstairs, 'upstairs')
    allData(downstairs, 'downstairs')
    print(x.shape)
    x.to_csv('.\ml_input_data.csv', index=False)

if __name__ == '__main__':
    createMlData()
