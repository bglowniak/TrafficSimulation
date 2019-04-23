import pandas as pd
import matplotlib.pyplot as plt
import os.path


def analyze(sim_times, traversal_times, sources, dests):
    if not os.path.exists('data_out'):
        os.makedirs('data_out')

    df = pd.DataFrame({'sim_time': sim_times, 'traversal_time': traversal_times,
                            'source': sources, 'dest': dests})
    
    df['windowed_avg'] = df['traversal_time'].rolling(500, min_periods=10).mean()

    df.to_csv(os.path.join('data_out', "data.csv"))
    plt.plot(df['sim_time'], df['windowed_avg'])
    plt.xlabel('Simulation Time')
    plt.ylabel('Traversal Time')
    plt.savefig(os.path.join('data_out', 'pre_clip.png'))
    plt.close()

    plt.plot(df['sim_time'], df['traversal_time'])
    plt.xlabel('Simulation Time')
    plt.ylabel('Traversal Time')
    plt.savefig(os.path.join('data_out', 'choppy_traversal.png'))
    plt.close()

    #df_valid = df.iloc[2000:].reset_index(drop=True)
    df_valid = df[df['sim_time'] > 1000]
    plt.plot(df_valid['sim_time'], df_valid['windowed_avg'])
    plt.xlabel('Simulation Time')
    plt.ylabel('Traversal Time')
    plt.savefig(os.path.join('data_out', 'post_clip.png'))
    plt.close()

    avg = df_valid['traversal_time'].mean()
    std = df_valid['traversal_time'].std()
    print('average: {:.2f}'.format(avg))
    print('std dev: {:.2f}'.format(std))

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

if __name__ == '__main__':
    analyze_NGSim_test_data()
