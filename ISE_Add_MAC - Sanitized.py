#BEGIN IMPORTS
import requests
import base64
import urllib3
import json
import re
from getpass import getpass
#END IMPORTS




#Suppress insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#BEGIN USER INSTRUCTIONS
print("1. You must be on the ASU VPN to use this tool")
print("2. Provide admin credentials for ISE")
print("3. Then provide the MAC address of the device you want to add, format it like so: XX:XX:XX:XX:XX:XX or XXXXXXXXXXXX")
print()
#END USER INSTRUCTIONS





#variables
username = input("Username: ")
password = getpass("Password: ")
mac = input("MAC ADDRESS: " )
creds = username + ":" + password
encodedBytes = base64.b64encode(creds.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")
api_url = "https://INSERTURLHERE:9060/ers/config/endpoint"
http_headers = {"Authorization": "Basic " + encodedStr}
body = {
	"ERSEndPoint": {
	"name": mac,
	"description": "test endpoint",
	"mac": mac,
	"staticProfileAssignment": False,
	"customAttributes": {
		"customAttributes": {
			"attr_str": "aaa",
			"attr_int": "111"
			}
		}
	}
}


#BEGIN INPUT VALIDATION
MACvalid = False
if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
	MACvalid = True
#END INPUT VALIDATION

#formatted for ISE ESR response
if MACvalid == True:
	response = requests.post(url=api_url, json=body, verify=False, headers=http_headers)
	if response.status_code == 201:
		print("Success, " + mac + " has been added to ISE")
	elif response.status_code == 500:
		print(mac + " was not added, most likely because it is already there. Check the ISE portal for more detail")
	elif response.status_code == 401:
		print("You failed to authenticate, are you using the correct username and password?")
	elif response.status_code == 400:
		print("Are you formatting your MAC address correctly? Use this format: XX:XX:XX:XX:XX:XX or XXXXXXXXXXXX")
else:
	print("Please provide a valid MAC address formatted like so: XX:XX:XX:XX:XX:XX or XXXXXXXXXXXX")





#Uncomment for more detailed response from server
#print(response.text)




