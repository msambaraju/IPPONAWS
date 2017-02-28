'''
Created on Feb 18, 2017

'''
import awsconnections
import json
import time
from boto.exception import BotoServerError

def createStackOnly(stackname, url, parameters, accesskey, secretkey, rollbacktimeout):
    cfConn = awsconnections.getCloudFormationConnection(awsAccessKey=accesskey, awsSecretKey=secretkey)
    
    output = checkStackExists(cfConn, stackname)
    if output['StackId'] != 'None':
        return output['StackId']
    
    disableRollback = False 
    
    stackid = cfConn.create_stack(stackname, template_url = url, parameters= parameters.items(), 
                        disable_rollback = disableRollback, timeout_in_minutes = rollbacktimeout)
    awsconnections.closeCloudFormationConnection(cfConn)
    return stackid

def checkStackExists (cfConn , stackname):
    cloudFormationOutput = {};
    try :
        stacks = cfConn.describe_stacks(stackname)
        if len(stacks) == 1 :
            stack = stacks[0]
            if stack.stack_status == 'CREATE_COMPLETE':
                cloudFormationOutput['StackId'] = stack.stack_id
                for output in stack.outputs:
                    cloudFormationOutput[output.key] = output.value
            else :
                raise Exception ("Stack with status "+ stack.stack_status + " exists")
        elif len(stacks) == 0 :
                cloudFormationOutput['StackId'] = 'None'
        else :
            raise Exception ("Multiple stacks found")
    except BotoServerError as err:
        if err.message.endswith('does not exist') :
            cloudFormationOutput['StackId'] = 'None'
        else :
            raise Exception (err)
        
    return cloudFormationOutput       
 

def createStackAndWaitForStatus(stackname, url, parameters, accesskey, secretkey, rollbacktimeout, waittime):
    cfConn = awsconnections.getCloudFormationConnection(awsAccessKey=accesskey, awsSecretKey=secretkey)
    #stackName = "TestStack"
    output = checkStackExists(cfConn, stackname)
    if output['StackId'] != 'None':
        return output
    
    disableRollback = False 
    cloudFormationOutput = {}
    cfConn.create_stack(stackname, template_url = url, parameters= parameters.items(), 
                        disable_rollback = disableRollback, timeout_in_minutes = rollbacktimeout)
    
    count = 0
    finished = False
    while (count < 9 and finished == False):
        stacks = cfConn.describe_stacks(stackname)
        if len(stacks) == 1 :
            stack = stacks[0]
            if stack.stack_status == 'CREATE_COMPLETE':
                finished=True
                cloudFormationOutput['StackId'] = stack.stack_id
                #print stack.stack_status
                for output in stack.outputs:
                    #print('%s=%s (%s)' % (output.key, output.value, output.description))
                    cloudFormationOutput[output.key] = output.value
            elif stack.stack_status.endswith('_FAILED') or \
                stack.stack_status in ('ROLLBACK_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE'):
                #print "Failed to create stack found invalid status" + stack.stack_status
                finished = True
                raise "Failed to create stack", stackname
            else:
                #print "Found In progress status" + stack.stack_status
                #print stack.stack_status
                count = count+1
                #print "sleeping for some time"
                time.sleep(int(waittime)) 
                #print "woke up from sleep"
        else :
            finished = True
            raise "Invalid stack name", stackname

    cloudFormationOutputJson = json.dumps(cloudFormationOutput)
    awsconnections.closeCloudFormationConnection(cfConn)
    return cloudFormationOutputJson

                                
def deleteStackAndWaitForStatus(stackid, accesskey, secretkey, waittime):
    cfConn = awsconnections.getCloudFormationConnection(awsAccessKey=accesskey, awsSecretKey=secretkey)
    cloudFormationOutput = {}
    cfConn.delete_stack(stackid)
    count = 0
    finished = False
    while (count < 9 and finished == False):
        try :
            stacks = cfConn.describe_stacks(stackid)
            if len(stacks) == 1 :
                stack = stacks[0]
                if stack.stack_status == 'DELETE_COMPLETE':
                    finished=True
                    #print stack.stack_status
                    for output in stack.outputs:
                        #print('%s=%s (%s)' % (output.key, output.value, output.description))
                        cloudFormationOutput[output.key] = output.value
                elif stack.stack_status.endswith('_FAILED') or \
                    stack.stack_status in ('ROLLBACK_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE'):
                    #print "Failed to create stack found invalid status" + stack.stack_status
                    finished = True
                    raise "Failed to delete stack", stackid
                else:
                    #print "Found In progress status" + stack.stack_status
                    #print stack.stack_status
                    count = count+1
                    #print "sleeping for some time"
                    time.sleep(int(waittime)) 
                    #print "woke up from sleep"
            else :
                finished = True
        except BotoServerError as err:
            if err.message.endswith('does not exist') :
                cloudFormationOutput['StackId'] = 'None'
                finished = True
            else :
                raise Exception (err)
            #if describe does not return any results assume it is deleted.

    cloudFormationOutputJson = json.dumps(cloudFormationOutput)
    awsconnections.closeCloudFormationConnection(cfConn)
    return cloudFormationOutputJson                  