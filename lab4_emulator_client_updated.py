# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 0
device_end = 5

#Path to the dataset, modify this
data_path = "data2/vehicle{}.csv"

#Path to your certificates, modify this
#certificate_formatter = "./certificates/device{}-certificate.pem"
#key_formatter = "./certificates/device{}-private.pem"
certificate_formatter = "./certificates/device{}-certificate.pem.crt"
key_formatter = "./certificates/device{}-private.pem.key"

##IoT config 
MY_IOT_ENDPOINT='a25du7fq9zim5c-ats.iot.us-east-2.amazonaws.com'
MY_IOT_ROOT_CA_PATH='./AmazonRootCA1.pem'


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint(MY_IOT_ENDPOINT, 8883)
        self.client.configureCredentials(MY_IOT_ROOT_CA_PATH, key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, Payload="{\"message\": \"This is from the program\"}"):
    #def publish(self, Payload="payload"):
        #TODO4: fill in this function for your publish
        #self.client.subscribeAsync("myTopic", 0, ackCallback=self.customSubackCallback)
        
        #self.client.publishAsync("myTopic", Payload, 0, ackCallback=self.customPubackCallback)

        for i in range(5): 
            topic_name = "vehicle/data/" + str(i)
            self.client.subscribeAsync(topic_name, 0, ackCallback=self.customSubackCallback)
        
        self.client.publishAsync("vehicle/data", Payload, 0, ackCallback=self.customPubackCallback)

print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    #print(a)
    data.append(a)
#print(len(data))
#print(data)


print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    #print(device_id)
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    client.client.connect()
    clients.append(client)
#print(clients) 

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            df = data[i]
            for index, row in df.iterrows():
                payload = "{\"vehicle\": " + str(i) + ", \"co2_emission\": " + str(row["vehicle_CO2"]) + "}"
                print(payload)
                c.publish(payload)

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)





