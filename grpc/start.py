import subprocess
import signal
import os
import logging
import time
import chat_pb2
import chat_pb2_grpc
import grpc
import pandas as pd

count = 8000

# Create a list to store all subprocesses
subprocesses = []

end_points = []
endpoint_health = {}

logging.basicConfig(filename='machine_log.txt', level=logging.INFO,
                    format='%(asctime)s %(message)s')



for i in range(5):
    end_points.append("localhost:"+str(count+i))
    subprocesses.append(subprocess.Popen(['python', 'server.py', '--p',str(count+i)]).pid)


# Function to kill all subprocesses
def kill_subprocesses():
    for process in subprocesses:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
print(subprocesses)


# Function to handle SIGINT signal
def sigint_handler(sig, frame):
    print("Ctrl+C detected, killing subprocesses...")
    kill_subprocesses()
    update_health()
# Register the SIGINT handler
signal.signal(signal.SIGINT, sigint_handler)



def check_health(endpoint):
    channel = grpc.insecure_channel(endpoint)
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    try:
        response = stub.CheckHealth(chat_pb2.HealthCheckResponse())
        if response.Status.SERVING == True:
            return True
        else:
            return False
    except grpc.RpcError:
        return False


def update_health():
    for endpoint in end_points:
        if check_health(endpoint):
            endpoint_health[endpoint] = True
            logging.info(f'{endpoint} is online')
        else:
            endpoint_health[endpoint] = False
            logging.info(f'{endpoint} is offline')
            
    df = pd.DataFrame.from_dict(endpoint_health, orient="index")
    df.to_csv("live_machines.csv", header=False)


out = dict(zip(end_points,subprocesses))
df = pd.DataFrame.from_dict(out, orient="index")
df.to_csv("crash_list.csv", header=False)
# with open("output.txt", "w") as file:
#     for k,item in zip(end_points,subprocesses):
#         file.write(str(item) + " , " (ite+ "\n")

while True: 
    time.sleep(.25)
    update_health()




