import json
import logging
import sys

import greengrasssdk

from collections import defaultdict

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

# Counter
my_counter = 0
max_emission_dict = defaultdict(float) 
def lambda_handler(event, context):
    global my_counter
    #TODO1: Get your data
    #Assume input of the form {"vehicle": 4, "co2_emission": 7692.05}
    vehicle_id = event['vehicle']
    co2_emission = event['co2_emission']

    #TODO2: Calculate max CO2 emission
    if max_emission_dict[vehicle_id] < co2_emission: 
        max_emission_dict[vehicle_id] = co2_emission

    my_counter += 1

    #TODO3: Return the result
    if my_counter >= 1675: 
        for keys in max_emission_dict.keys():
            topic_name = "vehicle/data/" + keys
            client.publish(
                topic=topic_name,
                payload=json.dumps(
                    {"message": "Max Co2 emission from vehicle {} is {}".format(keys, max_emission_dict[keys])}
                ),
            )

    return