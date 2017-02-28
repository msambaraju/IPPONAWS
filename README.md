## Synopsis

The experimental project contains artifacts to create a custom jenkins docker image with custom python scripts used to create and delete an aws cloudformation stack during the build process. The custom jenkins docker image is built on adding aws sdk and boto sdk on official jenkins base image. The custom jenkins image can execute any docker commands(to build, push, pull a docker image) on the docker host during the build process.

## Code Example

The custom cloudformation scripts takes arguments such as aws access keys, cloudformation stack template details, stack parameters e.t.c in order create a stack in the aws.


Below is an example gradle task which executes the script

    // aws access key
    def awsaccessKey = '--accesskey='+ awskey

    // aws secret key   
    def secretKey = '--secret='+ awssecret

    // aws stack parameters in the form of key1:value1,key2:value2,key3:value3 e.t.c      
    def parameters = '--parameters='+ stackparams

    // aws stack name  
    def stack = '--stackname='+stackName 

    // aws stack rollback timeout
    def rbacktimeout = '--rollbacktimeout='+ rtimeout 

    // the waitime is the time in seconds to invoke the describe_events api to obtain the status of the stack creation once
    // completed status is found the output is returned 
    def waittime = '--waittime='+ looptime 

    // the s3bucket name where the template will be uploaded
    def bucketname = '--bucketname='+s3bucketname

    // the name of the template file
    def filename = '--s3filename=' +s3filename

    // the file location of the template file.
    def fileloc = '--s3fileloc='+s3filelocation

    task createAWSStack(type:Exec) {
       workingDir './template/' // this is the working directory where a template exists
       executable = "python" 
       args = [script, awsaccessKey, secretKey, parameters, stack, rbacktimeout, waittime, bucketname,filename, fileloc]
    
       standardOutput = new ByteArrayOutputStream()
	   doLast {
	       ext.stackOutput = standardOutput.toString() // returns the stack outputs once it is created.
	       def object = jsonSlurper.parseText(stackOutput) 
	    // populate the values as needed from the stack outputs
	   }
    } 

The below code snippet is used to delete a stack

    task deleteAWSStack(type:Exec) {
       executable = "python"
       args = [script, awsaccessKey, secretKey, stack]
    
       standardOutput = new ByteArrayOutputStream()
	   doLast {
		ext.deleteResult = standardOutput.toString()
		println "Deleted the stack"
	   }
     }

## Motivation

The idea behind the project is to be able to build, create aws environment and deploy a microservice into it. 
Once a aws stack is created a task can be created to ssh into an docker host and execute the docker commands as
needed. Below is the sample gradle script to ssh. If remote API is enabled on the docker host then api can be invoked
instead of ssh.




    remotes {
      docker {
        user = awsuser   // get the user information from stack output or (ec2-user/ubuntu) based on the instance being created
        identity = file(awskeyfile) // get the private key file (fully qualified path)
      }
    }

    def command = 'docker run -d -p 80:8080 ' + org + "/" + jar.baseName

    task runDockerImage (dependsOn: createAWSStack) {
      doFirst {
       //read the host information from the stack created and use it for ssh
       remotes.docker.host = createAWSStack.sshHost
      }
      doLast {
	     ssh.run {
	     session(remotes.docker) {
	     // Execute a command
	      def result = execute command
	      println result
	    }
	   }
     }
    }




## Installation

A docker image can be pulled from the registry or the image can be built using the Dockerfile in the project. The docker image can be run
using the below command

    docker run --name myjenkins -d -p 80:8080 -v /tmp:/var/jenkins_home -v var/run/docker.sock:/var/run/docker.sock <image name>
