#!/usr/bin/python

'''\nCloudformation script usage
Arguments are needed to execute the script
'''   
import getopt
import sys
  

# accesskey, secret,keyname, stackname, rollbacktimeout, waittime
options, remainder = getopt.getopt(sys.argv[1:], '', ['accesskey=','secret=','keyname=','stackname=','rollbacktimeout=','waittime=',
                                                      'stackname=','filename=','fileloc=', 'bucketname=','parameters='])
    
if len(options) == 0 :
    print sys.exit(__doc__)
    raise Exception("Required arguments not provided")
    

for opt, arg in options:
    if opt == '--accesskey':
        accessKey = arg
    elif opt =='--secret':
        secretKey = arg
    elif opt == '--stackname':
        stackName= arg
    elif opt == '--bucketname':
        bucketname= arg
    elif opt == '--filename' :
        filename = arg
    elif opt == '--fileloc':
        filelocation = arg
    elif opt == '--rollbacktimeout':
        rollbacktimeout = arg
    elif opt == '--waittime':
        waittime = arg
    elif opt == '--parameters':
        stackparams = arg

#print accessKey
#print secretKey
#print stackName
#print rollbacktimeout
#print waittime
#print stackparams

parameters = {}

allparams = stackparams.split(',')
for eachparam in allparams:
    stackparam = eachparam.split(':')
    parameters[stackparam[0]] = stackparam[1]
        

import ippons3
import ipponcloudformation

s3url = ippons3.uploadFile(accessKey, secretKey, bucketname, filename, filelocation)

#print s3url

output = ipponcloudformation.createStackAndWaitForStatus(stackName, s3url, parameters, 
                                                accessKey, secretKey, rollbacktimeout, waittime)
print output

