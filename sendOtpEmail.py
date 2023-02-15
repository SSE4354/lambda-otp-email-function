import json
import boto3
import json

client = boto3.client("ses")


def lambda_handler(event, context):
    print(event)
    if(event['Records'][0]['eventName']=='INSERT'):
        mail_id=event['Records'][0]['dynamodb']['Keys']['email_id']['S']
        print("Email : {}".format(mail_id))
        
        otp=event['Records'][0]['dynamodb']['NewImage']['OTP']['N']
        print("OTP : {}".format(otp))
        
        body = """
                Use this OTP to verify your payment at Merchant2U shop.<br>This OTP Valid for 5 minutes. NEVER share this OTP with others.<br><br>
                
                OTP : <strong>{}
             """.format(otp)
             
        message = {"Subject": {"Data": 'MyBank2U: OTP Verification'}, "Body": {"Html": {"Data": body}}}
        
        response = client.send_email(Source = 'faizallmdsalleh@gmail.com', Destination = {"ToAddresses": [mail_id]}, Message = message) 
        
        print("The mail is sent successfully")