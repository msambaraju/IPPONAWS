#!/usr/bin/python

'''\nCloudformation script usage
Arguments are needed to execute the script
'''   

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--accesskey')
parser.add_argument('--secret')
parser.add_argument('--keyname')
parser.add_argument('--stackname')
parser.add_argument('--rollbacktimeout')
parser.add_argument('--waittime')
parser.add_argument('--s3filename')
parser.add_argument('--s3fileloc')
parser.add_argument('--bucketname')
parser.add_argument('--parameters')
parser.add_argument('--task')

myargs = parser.parse_args()
  

# accesskey, secret,keyname, stackname, rollbacktimeout, waittime
'''options, remainder = getopt.getopt(sys.argv[1:], '', ['accesskey=','secret=','keyname=','stackname=','rollbacktimeout=','waittime=',
                                                      'stackname=','s3filename=','s3fileloc=', 'bucketname=','parameters='])
    
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
        stackparams = arg'''

#print accessKey
#print secretKey
#print stackName
#print rollbacktimeout
#print waittime
#print stackparams

parameters = {}

allparams = myargs.parameters.split(',')
for eachparam in allparams:
    stackparam = eachparam.split(':')
    parameters[stackparam[0]] = stackparam[1]
        

import ippons3
import ipponcloudformation

if myargs.task == 'deletestack' :
    ipponcloudformation.deleteStackAndWaitForStatus(myargs.stackname, myargs.accesskey, myargs.secret, myargs.waittime)
else :
    s3url = ippons3.uploadFile(myargs.accesskey, myargs.secret, myargs.bucketname, myargs.s3filename, myargs.s3fileloc)

    output = ipponcloudformation.createStackAndWaitForStatus(myargs.stackname, s3url, parameters, 
                                                myargs.accesskey, myargs.secret, myargs.rollbacktimeout,                                                 myargs.waittime)
    print output

