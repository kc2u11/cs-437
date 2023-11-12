import boto3
import json

session = boto3.Session(profile_name='kc-iot')
thingClient = session.client('iot')


response = thingClient.list_certificates(
    pageSize=50,
    #marker='string',
    ascendingOrder=True
)
print(len(response['certificates']))
for element in response['certificates']: 
    arn = element['certificateArn']
    print(arn)
    response = thingClient.detach_principal_policy(
        policyName='KC_IoT_Policy',
        principal=arn
    )