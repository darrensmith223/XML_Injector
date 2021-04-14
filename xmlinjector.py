import requests
import json
import getopt
import sys
import xml.etree.ElementTree as ET


def sendTemplate(apiKey, recipientAddress, substitutionData, templateDict):
    # Construct Email Components
    campaignId = templateDict["campaignId"]
    templateId = templateDict["templateId"]

    # Construct API Call
    apiURL = "https://api.sparkpost.com/api/v1/transmissions"
    apiHeaders = {"Authorization": apiKey, "Content-Type": "application/json"}
    apiData = {
        "campaign_id": campaignId,
        "recipients": [
            {
                "address": {
                    "email": recipientAddress
                },
                "substitution_data": substitutionData
            }
        ],
        "content": {
            "template_id": templateId
        }
    }

    apiDataJson = json.dumps(apiData)

    # Send Email
    response = requests.post(apiURL, data=apiDataJson, headers=apiHeaders)
    if response.status_code != 200:
        print("Something went wrong: " + response.reason)


def readXMLData(sourceFile, recordTag):
    tree = ET.parse(sourceFile)
    root = tree.getroot()
    completeData = []  # list that will contain substitution data as JSON objects

    for record in root.iter(recordTag):  # loop through recipient records to accommodate large sends
        substitutionData = {}  # dictionary that will contain substitution data for a single recipient record
        for field in record.iter():  # loop through each substitution field within a record
            if field.tag != record.tag:
                substitutionData[field.tag] = field.text  # add field to JSON object
        completeData.append(substitutionData)  # add JSON object to list

    return json.dumps(completeData)


def manageArgs(argv):
    opts, args = getopt.getopt(argv, "hk:s:t:c:")

    instructions = "xmlinjector.py -k <api_key> -s <source_file_path> -t <templateId> -c <campaignId>"
    argsArray = []

    for opt, arg in opts:
        if opt == '-h':
            sys.exit()
        elif opt == "-k":
            apiKey = arg
            argsArray.append(apiKey)
        elif opt == "-s":
            sourceFile = arg
            argsArray.append(sourceFile)
        elif opt == "-t":
            templateId = arg
            argsArray.append(templateId)
        elif opt == "-c":
            campaignId = arg
            argsArray.append(campaignId)

    if len(argsArray) == 4:
        return argsArray
    else:
        print("incorrect number of arguments: " + instructions)


if __name__ == "__main__":
    # Initialize variables
    argArray = manageArgs(sys.argv[1:])  # pull parameters
    apiKey = argArray[0]
    sourceFile = argArray[1]
    templateId = argArray[2]
    campaignId = argArray[3]
    recordTag = "record"  # tag within XML file that will be used to identify a specific recipient record
    emailAddrTag = "emailAddr"  # tag within XML record to identify email address of recipient
    recpSubData = readXMLData(sourceFile, recordTag)  # Load XML Data from file
    jsonFile = json.loads(recpSubData)

    for recipientRecord in jsonFile:
        recipientAddress = recipientRecord[emailAddrTag]
        substitutionData = recipientRecord
        templateDict = {
            "campaignId": campaignId,
            "templateId": templateId
        }
        sendTemplate(apiKey, recipientAddress, substitutionData, templateDict)  # send email (stored template)
