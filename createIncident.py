#!/usr/bin/env python
"""
createIncident is Created on November 01 2017 8:51 PM using IDE PyCharm Community Edition

@author         : Himanshu Ranjan
@description    : This Python script creates a servicenow incident directly from the python3.6 script
@change tag     : None
"""

# Before using requests you need to install the requests package for python
import requests

# Set the request parameters
url = 'https://<your_instance>.service-now.com/api/now/table/incident'
user = 'your_user_id'
pwd = 'your_password'

# Set proper headers
headers = {"Content-Type": "application/json", "Accept": "application/json"}

# Do the HTTP request
response = requests.post(url, auth=(user, pwd), headers=headers, data='{"short_description":"Test ServiceNow Incident"}')

# Check for HTTP codes other than 200
if response.status_code != 201:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
    exit()

# Decode the JSON response into a dictionary and use the data
print('Status:', response.status_code, 'Headers:', response.headers, 'Response:', response.json())
