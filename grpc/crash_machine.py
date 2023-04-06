import subprocess
import pandas as pd
import argparse
import os
import signal



df = pd.read_csv("crash_list.csv",header=None)






parser = argparse.ArgumentParser(description='Crash a node')
parser.add_argument('--p', type=int, help='Enter a Port number')
args = parser.parse_args()
print(args.p)
print(df)
pid = df.loc[df[0] == 'localhost:{}'.format(args.p)].index[0]
os.kill(pid,signal.SIGTERM)
# print("creashed",df.loc[df[0] == 'localhost:{}'.format(args.p)])

