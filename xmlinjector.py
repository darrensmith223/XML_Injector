import argparse

import requests
import json
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


if __name__ == "__main__":
    # Import Arguments - Command Line
    parser = argparse.ArgumentParser(description="Send a message through SparkPost using XML formatted substitution data")
    parser.add_argument("apiKey", type=str, help="SparkPost API Key")
    parser.add_argument("sourceFile", type=str, help="Path to source XML file")
    parser.add_argument("templateId", type=str, help="Template_Id of SparkPost Stored Template")
    parser.add_argument("campaignId", type=str, help="Campaign_ID for transmission")

    args = parser.parse_args()

    apiKey = args.apiKey
    sourceFile = args.sourceFile
    templateId = args.templateId
    campaignId = args.campaignId
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
