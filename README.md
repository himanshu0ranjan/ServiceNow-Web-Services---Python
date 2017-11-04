# ServiceNow-Web-Services---Python
![Logo](https://docs.servicenow.com/static/custom/images/header-logo@2x.png?etag=x-_fu8_t)
My Servicenow Web Services Examples.

Here is some more detailed information about the scripts I have written for world famous IT service management tool Servicenow. In the scripts the comments etc are lined up correctly when they are viewed in Notepad++. 

createIncident.py - This Python script creates a servicenow incident directly from the python3.6 script. 
                    This requires the python requests package so, before using requests you need to install the
                    requests package for python3.6.

getIncident.py	  - This Python script gets the details of an Incident using incident number from ServiceNow
    	              tool and print the same on the Python console. This script is run from the command line and
                    the incident number is taken from the command line arguments/ copy clipboard.

sendOutlookMail.py - This Python script gets the details of an Incident using incident number from ServiceNow
                     tool and send the details to incident. The mail is sent to the user through Outlook mail client
                     in a particular format. The mail format is basically a template stored in the Outlook client
                     in the Template folder. This script is run from the command line and the incident number is
                     taken from the command line arguments/ copy clipboard.
