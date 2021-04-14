import responses
import xmlinjector


def readXMLFile():
    sourceFile = "path_to_test_XML"
    recordTag = "record"  # tag within XML file that will be used to identify a specific recipient record
    substitutionData = xmlinjector.readXMLData(sourceFile, recordTag)


@responses.activate
def sendMessage():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/transmissions',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    apiKey = "fake-key"
    recipientAddress = "fake-address"
    substitutionData = "fake-data"
    templateDict = "fake-template"
    xmlinjector.sendTemplate(apiKey, recipientAddress, substitutionData, templateDict)
