################################################### Connecting to AWS
import boto3

import json
################################################### Create random name for things
import random
import string
################################################### Session details 
#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#aws-iam-identity-center
#https://docs.aws.amazon.com/cli/latest/userguide/sso-configure-profile-token.html
#aws configure sso
#aws sso login --profile profile-name
my_profile='kc-iot'
################################################### Parameters for Thing
thingArn = ''
thingId = ''
defaultPolicyName = 'KC_IoT_Policy'
groupName = 'KC_static_thing_group'
groupArn = 'arn:aws:iot:us-east-2:211717013798:thinggroup/KC_static_thing_group'
###################################################

def createThing(pthingName, idx):
  global thingClient
  thingResponse = thingClient.create_thing(
      thingName = pthingName
  )
  data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
  #print(data)
  for element in data: 
    #print(element)
    if element == 'thingArn':
        thingArn = data['thingArn']
    elif element == 'thingId':
        thingId = data['thingId']
  print(thingArn, thingId)
  createCertificate(pthingName, idx)

def createCertificate(pthingName, idx):
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(
			setAsActive = True
	)
	data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
	for element in data: 
		if element == 'certificateArn':
			certificateArn = data['certificateArn']
		elif element == 'keyPair':
			PublicKey = data['keyPair']['PublicKey']
			PrivateKey = data['keyPair']['PrivateKey']
		elif element == 'certificatePem':
			certificatePem = data['certificatePem']
		elif element == 'certificateId':
			certificateId = data['certificateId']
	baseFile = './certificates/device' + str(idx) #pthingName
	public_key_name = baseFile + '-public.pem.key' # 'public.key'
	private_key_name = baseFile + '-private.pem.key' #'private.key'
	cert_name = baseFile + '-certificate.pem.crt' # 'cert.pem'				
	with open(public_key_name, 'w') as outfile:
		outfile.write(PublicKey)
	with open(private_key_name, 'w') as outfile:
		outfile.write(PrivateKey)
	with open(cert_name, 'w') as outfile:
		outfile.write(certificatePem)
	with open('list_devices.txt', 'a') as textfile:
		textfile.write(str(idx))
		textfile.write('\t')
		textfile.write(pthingName)
		textfile.write('\n')

	response = thingClient.attach_policy(
			policyName = defaultPolicyName,
			target = certificateArn
	)
	response = thingClient.attach_thing_principal(
			thingName = thingName,
			principal = certificateArn
	)
	response = thingClient.add_thing_to_thing_group(
        thingGroupName=groupName,
        thingGroupArn=groupArn,
        thingName=thingName,
        thingArn=thingArn,
        overrideDynamicGroups=True
    )

session = boto3.Session(profile_name=my_profile)
thingClient = session.client('iot')
for i in range(0,5):
	thingName = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
	print(thingName)
	createThing(thingName, i)