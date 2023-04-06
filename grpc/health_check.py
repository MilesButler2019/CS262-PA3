import consul 
import chat_pb2
import chat_pb2_grpc
import grpc

endpoint_health = {}

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
    for endpoint in endpoints:
        if check_health(endpoint):
            endpoint_health[endpoint] = True
        else:
            endpoint_health[endpoint] = False


# print(update_health)


# 
count = 8000
for i in range(5):
    print("127.0.0.1:"+str(count+i),check_health("127.0.0.1:"+str(count+i)))