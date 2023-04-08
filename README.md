# CS262-PA3

## Sytem Design
<img width="669" alt="Screen Shot 2023-04-08 at 4 40 37 PM" src="https://user-images.githubusercontent.com/47306315/230741714-b01b325d-8a51-42bb-bccb-c3cb06c17054.png">




# 4/4 
Today I started working on the assignment, my original idea is to implement a client side load balancing system from scratch. I decided to go with the grpc implentation as it felt cleaner. Although after many errors with a networking package consul, I have decided to add my own health check to the backend by chaning the .proto file to add a new rpc "Health Check" to ensure the status of the server. I had to change the server file to take in command line argument to take in a port number. I quickley realized that in order to replicate the backend that the data sould not live on the backend in case of failure and this was a higher priority than a load balancer. 


# 4/5 
Today I decided to implement a database to hold both credientals and messages of our sytem to make the backend replicatable. I went with a MongoDB cluster that has 3 nodes a primary (master) node and two replicas that will vote and one will take over (become primary / master). This is hosted in the cloud and has one service endpoint which is easy to implement in our backend the link follow this format mongodb+srv://<username>:<password>@cluster0.6ax79dz.mongodb.net/?retryWrites=true&w=majority. We then use pymongo to write to the database. We changed every call that held data on the server to write or read from the database this involved many changes to the server.py file.


# 4/6 
After the backend was able to sucsessfully able to operate on the databse, we needed to replicate this. We first attempted to replicate the servers all locally although after re reading the requirments on canvas and seeing that the severs need to be on one or more machines we decided to host all of our backends on AWS as that is more realistic. It was a bit difficult to figure out opening the correct ports but after a while we were able to get our backend to work on 1 ec2 instance. We then realized that there was a built in load balancers for aws. We then made 2 more ec2 instances and added them to a target group and configured health checks. Then we made a load balancer that balances the load between the ec2 instances. We then modified the server ip in the new_client.py file to the load balancer at Chat-Balancer-78072138f4f5371d.elb.us-east-1.amazonaws.com:8500.

# 4/8 
Today we tested automatic failover, by crashing ec2 instances and crashing the databse nodes. We also made some diagrams and updated tests.
