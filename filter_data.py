import numpy as np
import pandas as pd
from scipy import signal
import re
import os
import glob
import sys
from pathlib import Path
import matplotlib.pyplot as plt

features = ['gFx','gFy','gFz','ax','ay','az','wx','wy','wz']

def remove_outliers(df):
    # return df.loc[(df['time'] > 2.00) & (df['time'] < (df['time'].max() - 2.00) )].reset_index(drop=True)
    len = df.shape[0]
    df = get_fixed_portion(df, 300, len-300)
    return df

def get_fixed_portion(df, start, end):
    df = df.loc[start:end+1]
    return df


# Butterfly filter https://ggbaker.ca/data-science/content/filtering.html#filtering
def remove_noise_with_butterworth_filter(df):
    for col in features:
        b, a = signal.butter(3, 0.8, btype='lowpass', analog=False)
        df[col] = signal.filtfilt(b, a, df[col])
    return df

def get_subject_and_foot(filename):
    base  = os.path.basename(filename)
    base = base.split(".")
    subject = base[0].split('_')
    subject, foot, secs = subject[2], subject[1], subject[3]

    return (subject, foot, secs)

def plot_data(df):
        # df.plot(x = "time", y = features[:3],  title = "G-Force")
        df.plot(x = "time", y = features[3:6],  title = "Linear Acceleration")
        # df.plot(x = "time", y = features[6:9], ,title ="Angular Velocity")
        plt.show()

def get_file(filename):
    file = filename.strip('')



def main():

    walk_folder = str(Path('./Raw_data/walk/*.csv'))
    upstairs_folder = str(Path('./Raw_data/upstairs/*.csv'))
    downstairs_folder = str(Path('./Raw_data/downstairs/*.csv'))

    walk_data_files = glob.glob(walk_folder)
    upstair_data_files = glob.glob(upstairs_folder)
    downstair_data_files = glob.glob(downstairs_folder)


    #walk_data
    list_ = []
    for filename in walk_data_files:
        print ("processing file: ", filename)


        # read csv and drop null values
        walk_df = pd.read_csv(filename, index_col=None, header=0).dropna(axis=0)

        subject, foot, secs = get_subject_and_foot(filename)


        walk_df= walk_df.assign(subject_number = subject, foot = foot)

        # keep data within a certain time period, this hopefully gets rid of outliers

        walk_df = remove_outliers(walk_df)


        # remove noise using butterworth filter
        walk_df = remove_noise_with_butterworth_filter(walk_df)

        #keep fixed portiin of data
        start = 400
        end = 1900
        for i in range(0,10):

            df = get_fixed_portion(walk_df, start, end)
            name = 'walk_' + foot + '_' + subject + '_' + secs + '_' + str(i) + '.csv'
            clean_folder= str(Path('./filtered_data/walk/' + name))
            df.to_csv(os.path.join(clean_folder), index=False)

            start += 750
            end += 750


        # name = 'walk_' + foot + '_' + subject + '_' +secs + '.csv'
        # clean_folder= str(Path('./filtered_data/walk/' + name))
        # walk_df.to_csv(os.path.join(clean_folder), index=False)

        list_.append(walk_df)

    walk_df = pd.concat(list_, axis=0, ignore_index=True)
    # print(walk_df)

    #upstairs_data
    list_ = []
    for filename in upstair_data_files:
        print ("processing file: ", filename)
        # read csv and drop null values
        stairs_df = pd.read_csv(filename, index_col=None, header=0).dropna(axis = 0)
        subject, foot, secs = get_subject_and_foot(filename)
        stairs_df = stairs_df.assign(subject_number = subject, foot = foot)

        # keep data within a certain time period, this hopefully gets rid of outliers
        stairs_df = remove_outliers(stairs_df)
        # remove noise using butterworth filter
        stairs_df = remove_noise_with_butterworth_filter(stairs_df)
        #keep fixed portiin of data
        start = 400
        end = 1900
        for i in range(0,10):

            df = get_fixed_portion(stairs_df, start, end)
            name = 'upstairs_' + foot + '_' + subject + '_' + secs + '_' + str(i) + '.csv'
            clean_folder= str(Path('./filtered_data/upstairs/' + name))
            df.to_csv(os.path.join(clean_folder), index=False)

            start += 750
            end += 750


        # name = 'stairs_' + foot + '_' + subject + '.csv'
        # clean_folder= str(Path('./filtered_data/stairs/' + name))
        # stairs_df.to_csv(os.path.join(clean_folder), index=False)

        #append
        list_.append(stairs_df)


    stairs_df = pd.concat(list_, axis=0, ignore_index=True)
    # print(stairs_df)

    #downstairs_data
    list_ = []
    for filename in downstair_data_files:
        print ("processing file: ", filename)

        # read csv and drop null values
        stairs_df = pd.read_csv(filename, index_col=None, header=0).dropna(axis = 0)
        subject, foot, secs = get_subject_and_foot(filename)
        stairs_df = stairs_df.assign(subject_number = subject, foot = foot)

        # keep data within a certain time period, this hopefully gets rid of outliers
        print(stairs_df.shape)
        stairs_df = remove_outliers(stairs_df)
        print(stairs_df.shape)
        # remove noise using butterworth filter
        stairs_df = remove_noise_with_butterworth_filter(stairs_df)
        #keep fixed portiin of data
        start = 400
        end = 1900
        for i in range(0,10):

            df = get_fixed_portion(stairs_df, start, end)
            print(df.shape)
            name = 'downstairs_' + foot + '_' + subject + '_' + secs + '_' + str(i) + '.csv'
            clean_folder= str(Path('./filtered_data/downstairs/' + name))
            df.to_csv(os.path.join(clean_folder), index=False)

            start += 750
            end += 750


        # name = 'stairs_' + foot + '_' + subject + '.csv'
        # clean_folder= str(Path('./filtered_data/stairs/' + name))
        # stairs_df.to_csv(os.path.join(clean_folder), index=False)

        #append
        list_.append(stairs_df)


    stairs_df = pd.concat(list_, axis=0, ignore_index=True)
    # print(stairs_df)

    print ("SUCCESFULLY PROCESSED ALL THE FILES!")

    # plot_data(walk_df)

    # clean_folder= str(Path('./filtered_data/all_walk_data.csv'))
    # walk_df.to_csv(os.path.join(clean_folder ) ,index=False)
    # clean_folder= str(Path('./filtered_data/all_stairs_data.csv'))
    # stairs_df.to_csv(os.path.join(clean_folder), index=False)


if __name__ == '__main__':
    main()
