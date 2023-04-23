import xml.etree.ElementTree as ET
import pandas as pd
import csv
import boto3  
import os
import logging

logging.basicConfig(filename='example.log', level=logging.INFO)
# Parse the XML file
try:
    tree = ET.parse('C:/Users/uditc/Desktop/steeleye/steeleye.xml')
    root = tree.getroot()
# Open the CSV file for writing
    with open('myfile.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
# Write the header row
        writer.writerow(['FinInstrmGnlAttrbts.Id', 'FinInstrmGnlAttrbts.FullNm', 'FinInstrmGnlAttrbts.ClssfctnTp', 'FinInstrmGnlAttrbts.CmmdtyDerivInd', 'FinInstrmGnlAttrbts.NtnlCcy', 'Issr'])
# Loop through the FinancialInstrument elements and write the data rows
        for termntd_rcrd in root.findall('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}TermntdRcrd'):
            id = termntd_rcrd.find('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}Id').text
            full_nm = termntd_rcrd.find('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}FullNm').text
            clssfctn_tp = termntd_rcrd.find('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}ClssfctnTp').text
            cmmdty_deriv_ind = termntd_rcrd.find('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}CmmdtyDerivInd').text
            ntnl_ccy = termntd_rcrd.find('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}NtnlCcy').text
            issr = termntd_rcrd.find('.//{urn:iso:std:iso:20022:tech:xsd:auth.036.001.02}Issr').text
            writer.writerow([id, full_nm, clssfctn_tp, cmmdty_deriv_ind, ntnl_ccy, issr])

    logging.info('CSV file created successfully')
except Exception as e:
    logging.error(f'Error occurred: {e}')
# Store the csv in an AWS S3 bucket
#install boto3 : allows you to directly create, update, and delete AWS resources from your Python scripts
 #uncomment while running it for the first time.
#!pip install botocore==1.13.20
try:
#if not able to access the access key and secret access key in case while creating USER in AWS through IAM user, 
#then for rrot user -> through security credentials can get the credentials and define it in the environment;
# otherwise it will throw an error. 
    os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAU6C5AWQKBV7DQIM6'
    os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
#To make a bucket in S3, follow steps:
# 1. Create an account on AWS as an IAM user (if not possible, then root user).
# 2. Click on Services, then under security-> IAM(Identity and Access Management)
# 3. Create a User from access management
#    3.1 ->Go to the Users tab.
#    3.2 ->Click on Add users.
#    3.3 ->Enter a username in the field.
#    3.4 ->Select the "Access key — Programmatic access field" (essential).
#    3.5 ->Click "Next" and "Attach existing policies directly."
#    3.6 ->Select the "AdministratorAccess" policy.
#    3.7 ->Click "Next" until you see the "Create user" button
#    3.8 ->Ultimately, download the given CSV file of your user's credentials.  
# 4. Create a bucket
#    4.1 -> Select Services -> Under Storage -> S3
#    4.2 -> Click "Create bucket" and give it a name
#    4.3 -> You can choose any region. Leave the rest settings as it is. 
#    4.4 -> Create a policy and add it to user
#    4.4.1 ->Go to the policies tab 
#    4.4.2 -> Click the "JSON" tab and insert the code below:{
#    "Version": "2012-10-17",
#   "Statement": [
#        {
#            "Sid": "ConsoleAccess",
#            "Effect": "Allow",
#            "Action": [
#                "s3:*"
#            ],
#            "Resource": [
#                "arn:aws:s3:::your-bucket-name",
#                "arn:aws:s3:::your-bucket-name/*"
#            ]
#        }
#    ]
#}
#   4.4.3 -> Go to the Users tab and click on the user we created in the last section. 
#   4.4.4 -> Click the "Add permissions" button.
#   4.4.5 -> Click the "Attach existing policies" tab.
#   4.4.6 -> Filter policies by the policy we just created.
#   4.4.7 -> Select the policy, review it and click "Add" the final time.
# 5. Download AWS CLI and configure your user
# 6. Open Terminal and run the command:
#         aws configure
#         AWS Access Key ID [None]: Your access key id
#         AWS Secret Access Key [None]: Your secret access key
#         Default region name [None]: Region  you've selected earlier
#         Default output format [None]: just enter
#      this will give no output.
#      C:\Users\study>aws configure list 
#      Name                    Value                Type    Location
#      ----                    -----                 ----    --------
#      profile                <not set>             None    None
#      access_key     **************** shared-credentials-file
#      secret_key     **************** shared-credentials-file
#      region US East (N. Virginia) us-east-1      config-file    ~/.aws/config
# 7. Upload your files using python scripts

# Let's use Amazon S3 -> resource is used for high level APIs and client is used for low level APIs
    s3 = boto3.resource("s3")
#bucket names
    for bucket in s3.buckets.all():
        logging.info(f'Bucket name: {bucket.name}')

    s3 = boto3.client('s3')
# to upload the file in AWS S3
    s3.upload_file(
        Filename="C:/Users/uditc/Desktop/steeleye/myfile.csv",
        Bucket="steeleyes3bucket",
        Key="myfile.csv",
    )
# We can successfully check under the bucket that file has uploaded.
    logging.info('File uploaded to S3 successfully')
except Exception as e:
    logging.error(f'Error occurred: {e}')
