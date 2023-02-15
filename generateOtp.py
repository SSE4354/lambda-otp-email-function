import json
import boto3
import time
import json
from random import randint

import datetime as dt
import dateutil.tz

client_dynamo=boto3.resource('dynamodb')

table=client_dynamo.Table('otp_holder')

default_ttl = 300
kl = dateutil.tz.gettz('Asia/Kuala_Lumpur')
date_now = dt.datetime.now(tz=kl)

def lambda_handler(event, context):
    
    email_id=event['queryStringParameters']['email']
    
    opt_expire_int=int(date_now.timestamp()) + default_ttl
    otp_value=randint(100000, 999999)
    opt_expire=dt.datetime.fromtimestamp(opt_expire_int, tz=kl).strftime('%Y-%m-%d %H:%M:%S')
    
    entry={
    'email_id': email_id,
    'OTP': otp_value,
    'EXPIRATION_TIME': opt_expire_int
    }
    
    response=table.put_item(Item=entry)

    value = {
        "success": "true",
        "status": "generated",
        "message": "OTP successfully generated",
        "email": email_id,
        "otp": otp_value,
        "opt_expire": opt_expire
    }


    # Dictionary to JSON Object using dumps() method
    # Return JSON Object
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(value)
    }
