import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os
currentdir = os.getcwd()
walking = os.path.join(currentdir, 'filtered_data/walk')
upstairs = os.path.join(currentdir, 'filtered_data/upstairs')
downstairs = os.path.join(currentdir, 'filtered_data/downstairs')
print (currentdir)
x = pd.DataFrame()

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

        # noise_filtered = noise_filtered.drop(['ax', 'ay', 'az'], axis = 1).copy()
        noise_filtered = noise_filtered.drop(['time', 'prev_time', 'del_t'], axis = 1).copy()
        noise_filtered = noise_filtered.drop(noise_filtered.index[0])

        noise_filtered = noise_filtered.values.flatten()
        noise_filtered = pd.DataFrame(noise_filtered).transpose()
        action_col = pd.DataFrame([[action]], columns=['action'])
        noise_filtered = pd.concat([action_col, noise_filtered], axis=1)
        print(noise_filtered.shape)
        x = x.append(noise_filtered)


        # print (noise_filtered.shape)
        # df_1 = noise_filtered#.iloc[:150,:]
        # print (df_1.shape)
        # df_2 = noise_filtered.iloc[225:,:]
        # print (df_2.shape)
        # scaler = StandardScaler()
        # X = scaler.fit_transform(X)
        # print(noise_filtered)

        # action_col = pd.DataFrame([[action]], columns=['action'])
        # df_1 = df_1.values.flatten()
        # df_1 = pd.DataFrame(df_1).transpose()
        # df_1 = pd.concat([action_col, df_1], axis=1)
        # x = x.append(df_1)
        # print("df_1", df_1)
        # df_2 = df_2.values.flatten()
        # df_2 = pd.DataFrame(df_2).transpose()
        # df_2 = pd.concat([action_col, df_2], axis=1)
        # x = x.append(df_2)

        # print (t)

        # print(i)
        # x = x.append(i)
        # x ['action'] = action
        # print (noise_filtered)



allData(walking, 'walking')
allData(upstairs, 'upstairs')
allData(downstairs, 'downstairs')
X = x.loc[:, x.columns != 'action']
y = x['action']

print (x)

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0, stratify = y)

model = KNeighborsClassifier(7)
model.fit(X_train, y_train)
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# y = pd.DataFrame()
# for filename in os.listdir(stairs):
#     print ("!!!!!!!!!!!!!!!!!!",filename)
#     file = os.path.join(walking, filename)
#     print (file)
#     data = pd.read_csv(file)
#     print (data)
#     noise_filtered = data[["ax","ay","az"]].copy()
#     print(noise_filtered)
#     t = noise_filtered.values.flatten()
#     print (t)
#     i = pd.DataFrame(t).transpose()
#     print(i)
#     y = y.append(i)
#     y ['action'] = 'staris'
# print (y)
