[![Build Status](https://travis-ci.com/darrensmith223/XML_Injector.svg?branch=master)](https://travis-ci.com/darrensmith223/XML_Injector)

# XML_Injector
Python-based tool designed as a simple command line tool that will send messages using stored templates through SparkPost, leveraging an XML file to pass contact information and substitution data.

# The XML File
## File Creation and Format
The contact information used for the mailing is stored as an XML file.  The file is created with each contact record separated using the tag "record".  Within a single record, each contact has an email address, stored as "emailAddr", and two substitution data variables - "firstName" and "lastName".  A sample XML file can be found below:

    <data>
        <record>
            <emailAddr>local1@domain.com</emailAddr>
            <firstName>First1</firstName>
            <lastName>Last1</lastName>
        </record>
        <record>
            <emailAddr>local2@domain.com</emailAddr>
            <firstName>First2</firstName>
            <lastName>Last2</lastName>
        </record>
    </data>


## Adding and Modifying Substitution Data
Substitution variables can be added by including the additional fields within a contact record in the XML file.  For example, if you wanted to include a substitution variable "country" to your template, the variable could be added to the XML file as shown below:

    <record>
        <emailAddr>local2@domain.com</emailAddr>
        <firstName>First2</firstName>
        <lastName>Last2</lastName>
        <country>Country_Name</country>
    </record>


The tool will read the tag names from the xml file and dynamically pass these as substitution data in the SparkPost transmission.  The substitution variables do not need to be uniform for each contact record, and not all substitution variables need to be used within the email template.

Note:  The xml tag for substitution variables must be the same as the substitution variable name used in the stored template.


## Altering the Record and Email Address Tags
The tool is designed with certain assumptions having been made regarding the format of a contact record within the XML file.  A few of these assumptions are as follows:

* Each contact record is separated using a uniform record tag.
* Each contact record includes an email address
* Each email address is stored within a contact record using a uniform field name

The tool expects that each contact record is separated using a uniform tag, and each record contains the email address stored with a uniform tag.  By default, the tool uses the tag "record" to identify a unique contact record, and the tag "emailAddr" to identify the email address; however, there may be cases where a different tag name should be used to identify a unique contact record or email address.

To change which tag name the tool should use, the respective tag name should be updated in the main script where these tag names are set:

```python
recordTag = "record"  # tag within XML file that will be used to identify a specific recipient record
emailAddrTag = "emailAddr"  # tag within XML record to identify email address of recipient
```


## Altering the XML Format
The tool is designed with the assumption that the XML file is formatted relatively flat, where each contact record is separated into a unique record, and that each record contains the substitution variables without any additional nested objects.  There may be scenarios in which the use of a more complex format is required.  In order to support such scenarios, the function "readXMLData" can be modified to accommodate the required format.


# The Email

The messages are sent using [SparkPost Stored Templates](https://www.sparkpost.com/docs/getting-started/creating-template/).  The mailings are sent as single-recipient messages.


## Expected Parameters
The command-line tool expects the following parameters:

* API key:  The [SparkPost API key](https://www.sparkpost.com/docs/getting-started/create-api-keys/) used to authenticate your mailing 
* Source File:  The full file path to the XML file where the contact records can be found
* Template ID:  The ID of the [SparkPost Stored Template](https://www.sparkpost.com/docs/getting-started/creating-template/) that should be used for this mailing
* Campaign ID:  The ID of the campaign that is being sent.  This will be used to reference the mailing within your SparkPost events and metrics data.


## Send a Message
To send an email using the XML_Injector command line tool, the first step is to create your XML file with the expected format and variables.  Once the XML file has been created, you can send a message by calling the tool from the command line and passing the expected parameters.  For example:

```
xmlinjector.py API_Key "/path/xml_file.xml" "welcome-email" "Welcome_Email"
```

# See Also
[SparkPost API Documentation](https://developers.sparkpost.com/api/)

