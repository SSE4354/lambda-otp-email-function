import json
import boto3
import time
import json
client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    
    email_id=event['queryStringParameters']['email']
    #print("The received email id : {}".format(email_id))
    
    otp_from_user=event['queryStringParameters']['otp']
    #print("The received otp : {}".format(otp_from_user))
    
    response = client.query(
    TableName='otp_holder',
    KeyConditionExpression='email_id = :email_id',
    ExpressionAttributeValues={
        ':email_id': {'S': email_id}
    },ScanIndexForward = False, Limit = 1)
    
    
    def responses():
        
        if(response['Count']==0):
            value = {
                "success": "false",
                "status": "empty",
                "message": "OTP not found",
                "error_code": "1306",
                "data": ""
            }            
        else:
            latest_stored_otp_value=response['Items'][0]['OTP']['N']
            #print("Latest Stored OTP Value : {}".format(latest_stored_otp_value))
            
            if(int(response['Items'][0]['EXPIRATION_TIME']['N'])<int(time.time())):
                value = {
                    "success": "false",
                    "status": "expired",
                    "message": "OTP Expired",
                    "error_code": "1306",
                    "data": ""
                }            
            else:
                if(latest_stored_otp_value==otp_from_user):
                    value = {
                        "success": "true",
                        "status": "verified",
                        "message": "OTP Verified",
                        "data": ""
                    }
                else:
                    value = {
                        "success": "false",
                        "status": "mismatched",
                        "message": "OTP Mismatched",
                        "error_code": "1306",
                        "data": ""
                    }   
                    
        return value
            
    # Dictionary to JSON Object using dumps() method
    # Return JSON Object
    # Call Function and Print it.
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(responses())
    }

    
    