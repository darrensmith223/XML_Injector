import responses
import xmlinjector


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
