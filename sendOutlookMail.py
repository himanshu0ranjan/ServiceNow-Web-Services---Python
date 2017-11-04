#! python3
"""
sendOutlookMail.py is Created on November 01 2017 8:59 PM using IDE PyCharm Community Edition

@author         : Himanshu Ranjan
@description    : This Python script gets the details of an Incident using incident number from ServiceNow
                  tool and send the details to incident. The mail is sent to the user through Outlook mail client
                  in a particular format. The mail format is basically a template stored in the Outlook client
                  in the Template folder. This script is run from the command line and the incident number is
                  taken from the command line arguments/ copy clipboard.
@change tag     : None
"""

import requests
import sys
import pyperclip
import psutil
import os
import subprocess
import win32com.client as win32


# Function to send the mail using Outlook template
def send_notification(name, email, incnumber, description):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItemFromTemplate('<your local directory template path>\\template.oft')
    mail.To = email
    mail.Cc = 'yourmail@example.com'
    mail.Subject = description + '-' + incnumber
    mailStr = mail.HTMLBody
    newStr = mailStr.replace('incidentnumber', incnumber)
    newStr = newStr.replace('incidentdesc', description)
    newStr = newStr.replace('username', name)
    mail.HTMLBody = newStr
    mail.send


# Function to open the Microsoft Outlook client in the system (Outlook.exe). Path may vary according to system config
# Please check the path to .exe file and update below
def open_outlook():
    try:
        subprocess.call(['C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE'])
        os.system("C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE")
    except FileNotFoundError:
        print("Outlook didn't open successfully")
        exit()


# Start of the program
url = 'https://<your_instance>.service-now.com/api/now/table/incident'
user = 'your_user_id'
pwd = 'your_password'

if len(sys.argv) > 1:
    #Get incident number from the command line
    incidentNumber = sys.argv[1]
else:
    #Get incident number from the clipboard
    incidentNumber = pyperclip.paste()

# Set proper headers
headers = {"Accept": "application/json"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers)

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
    exit()

jsonDataString = response.json()
jsonDataList = jsonDataString['result']

# Fetch the various details regarding incident from the connected ServiceNow instance
for i in range(len(jsonDataList)):
    for key, values in jsonDataList[i].items():
        if key == 'number' and str(values) == incidentNumber:
            incNumber = jsonDataList[i]['number']
            shortDescription = jsonDataList[i]['short_description']
            callerId = jsonDataList[i]['caller_id']
            assignmentGroup = jsonDataList[i]['assignment_group']
            break

# Do the HTTP request to get the Incident user details. From previous request we get only the link to the caller id
# for the incident. So, a separate request is required to get the required details from this caller id link.
userResponse = requests.get(callerId['link'], auth=(user, pwd), headers=headers)
# Check for HTTP codes other than 200
if userResponse.status_code != 200:
    print('Status:', userResponse.status_code, 'Headers:', userResponse.headers, 'Error Response:', userResponse.json())
    exit()

# Do the HTTP request to get the Incident assignment group details. From previous request we get only the link to
# the assignment group link for the incident. So, a separate request is required to get the required details
# from this assignment group link.
groupResponse = requests.get(assignmentGroup['link'], auth=(user, pwd), headers=headers)
# Check for HTTP codes other than 200
if groupResponse.status_code != 200:
    print('Status:', groupResponse.status_code, 'Headers:', groupResponse.headers, 'Error Response:', groupResponse.json())
    exit()

userDict = userResponse.json()['result']
groupDict = groupResponse.json()['result']
userName = userDict['name']
userEmail = userDict['user_name']
groupName = groupDict['name']
groupEmail = groupDict['email']
shortDescription = shortDescription

# Checking if outlook is already opened. If not, open Outlook.exe and send email
for item in psutil.pids():
    p = psutil.Process(item)
    if p.name() == "OUTLOOK.EXE":
        flag = 1
        break
    else:
        flag = 0

if flag == 1:
    send_notification(userName, userEmail, incNumber, shortDescription)
else:
    open_outlook()
    send_notification(userName, userEmail, incNumber, shortDescription)

print('Acknowledgement Mail Sent to % s' % userName)
