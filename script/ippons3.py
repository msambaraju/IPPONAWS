'''
Created on Feb 20, 2017

@author: malliksambaraju
'''
import awsconnections
from boto.s3.key import Key

def uploadFile (accesskey, secretkey, bucketname, filename, filelocation):
    s3conn = awsconnections.getS3Connection(awsAccessKey = accesskey, awsSecretKey = secretkey)
    bucket = s3conn.create_bucket(bucketname)
    bucketKey = Key(bucket)
    bucketKey.key = filename
    bucketKey.set_contents_from_filename(filelocation)
    s3url = "https://s3.amazonaws.com/"+bucketname+"/"+filename
    awsconnections.closeS3Connection(s3conn)
    return s3url