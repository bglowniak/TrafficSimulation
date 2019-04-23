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
    plt.savefig(os.path.join('data_out', 'pre_clip.png'))
    plt.close()

    df_valid = df.iloc[2000:].reset_index(drop=True)
    plt.plot(df_valid['sim_time'], df_valid['windowed_avg'])
    plt.savefig(os.path.join('data_out', 'post_clip.png'))
    plt.close()

    avg = df_valid['traversal_time'].mean()
    std = df_valid['traversal_time'].std()
    print('average: {:.2f}'.format(avg))
    print('std dev: {:.2f}'.format(std))
