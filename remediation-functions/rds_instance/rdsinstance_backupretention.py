'''
Copyright (c) Cloudneeti. All rights reserved.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is  furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

RDS Instance Backup Retention Period
'''
import time
from botocore.exceptions import ClientError

def run_remediation(rds, RDSInstanceName):
    print("Executing RDS instance remediation")
    response = ''
    current_retention = 0
    #Verify Current Backup retention
    try:
        response = rds.describe_db_instances(DBInstanceIdentifier = RDSInstanceName)['DBInstances']
        current_retention = response[0]['BackupRetentionPeriod']
    except ClientError as e:
        responseCode = 400
        output = "Unexpected error: " + str(e)
    except Exception as e:
        responseCode = 400
        output = "Unexpected error: " + str(e)  

    if current_retention < 7:
        #verify instance state  
        while response[0]['DBInstanceStatus'] not in ['available', 'stopped']:
            try:
                response = rds.describe_db_instances(DBInstanceIdentifier = RDSInstanceName)['DBInstances']
                time.sleep(10)
            except ClientError as e:
                responseCode = 400
                output = "Unexpected error: " + str(e)
            except Exception as e:
                responseCode = 400
                output = "Unexpected error: " + str(e)
                
        #Enabling Backup retention
        try:
            result = rds.modify_db_instance(
                DBInstanceIdentifier = RDSInstanceName,
                ApplyImmediately = True,
                BackupRetentionPeriod = 8
            )
            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                output = "Unexpected error: %s \n" % str(result)
            else:
                output = "Backup retention set to 7 days for rds-instance : %s \n" % RDSInstanceName
                    
        except ClientError as e:
            responseCode = 400
            output = "Unexpected error: " + str(e)
            print(output)
        except Exception as e:
            responseCode = 400
            output = "Unexpected error: " + str(e)
            print(output)
    else:
        responseCode = 200
        output = "RDS-instance already compliant"

    print(str(responseCode)+'-'+output)
    return responseCode,output