'''
Created on Feb 20, 2017

@author: malliksambaraju
'''
from boto.s3.connection import S3Connection
from boto.cloudformation.connection import CloudFormationConnection

def getS3Connection (awsAccessKey, awsSecretKey):
    s3conn = S3Connection(awsAccessKey, awsSecretKey)
    return s3conn

def closeS3Connection (s3Conn= S3Connection):
    s3Conn.close()


def getCloudFormationConnection (awsAccessKey, awsSecretKey):
    cloudFormationConnection = CloudFormationConnection(awsAccessKey, awsSecretKey)
    return cloudFormationConnection
    

def closeCloudFormationConnection (cloudFormationConnection= CloudFormationConnection):
    cloudFormationConnection.close()