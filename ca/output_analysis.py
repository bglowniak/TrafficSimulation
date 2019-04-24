import pandas as pd
import numpy as np
from scipy.stats import t
import matplotlib.pyplot as plt
import os.path
from driver import simulation

def analyze_NGSim_test_data():
    df = pd.read_csv('ngsim//Processed_Vehicle_Data_Validation.csv')
    #remove vehicles that start at intersection 5
    df = df[df['Intersection'] != 5]
    #remove vehicles that have an average speed of 0
    df = df[df['Avg_Velocity'] != 0]
    #remove vehicles whose start intersection equals their leave intersection
    df = df[df['Intersection'] != df['Intersection_Last']]
    #find vehicle traversal time in seconds
    df['traversal_time'] = round((df['Leave_Time'] - df['Epoch_ms'])/1000)
    #remove vehicles that take less than 2 seconds
    df = df[df['traversal_time'] > 1]

    avg = df['traversal_time'].mean()
    std = df['traversal_time'].std()
    print('average: {:.2f}'.format(avg))
    print('std dev: {:.2f}'.format(std))
    df.to_csv('ngsim//vehicle_travesal.csv')

def produce_confidence_interval():
    RUNS = 5

    runs = []
    for _ in range(RUNS):
        runs.append(simulation())

    avgs = []
    stds = []
    for arr in runs:
        #compute population means
        avgs.append(np.mean(arr))
        #compute population standard deviations
        stds.append(np.std(arr))
    #compute mean of the mean traversal times
    avg_avg = np.mean(avgs)
    print('average_average: {:.2f}'.format(avg_avg))
    #compute sample standard deviation of the mean traversal times
    avg_std = np.std(avgs, ddof=1)
    interval = t.interval(.95, len(arr)-1, loc=avg_avg, scale=avg_std)
    print(interval)
    avg_err = (interval[1] - avg_avg)
    print("distance from mean: {:.2f}".format(avg_err))

    #compute mean of the standard deviation traversal times
    std_avg = np.mean(stds)
    print('average_std: {:.2f}'.format(std_avg))
    #compute sample standard deviation of the mean traversal times
    std_std = np.std(stds, ddof=1)
    interval_std = t.interval(.95, len(arr)-1, loc=std_avg, scale=std_std)
    print(interval_std)
    std_err = interval_std[1] - std_avg
    print("distance from mean: {:.2f}".format(std_err))

    plot_confidence_intervals(avg_avg, avg_err, std_avg, std_err)


def plot_confidence_intervals(avg_avg, avg_err, std_avg, std_err):
    #avg_ngsim = 91.2
    plt.bar(['Mean', 'Standard Deviation'], [avg_avg, std_avg], width=.5, yerr=[avg_err, std_err], capsize=7)
    plt.show()

if __name__ == '__main__':
    #analyze_NGSim_test_data()
    produce_confidence_interval()
    #plot_confidence_intervals()
