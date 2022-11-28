import boto3
from datetime import datetime, timedelta
import time
import json
import base64, gzip
import re
from botocore.exceptions import ClientError
import os


def lambda_handler(event, context):
    
    client = boto3.client('logs')
    
    ## Print trigger event 
    print(f"Awslog: {event['awslogs']}")
    
    event_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(event_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    log_events = payload['logEvents']
    for log_event in log_events:
        print(f'LogEvent: {log_event}')
        print(f'LogEvent Type: {type(log_event)}')
        message = log_event['message']
        print(f'Log Message: {message}')
        print(f'Message Type: {type(message)}')
    
    if message != "":
        # Publish message to sns
        topic_arn = os.environ.get("SNS_TOPIC_ARN")
        print(f'Publishing message to topic - {topic_arn}...')
        message_id = publish_message(topic_arn, message)
        print(f'Message published to topic - {topic_arn} with message Id - {message_id}.')
    else:         
        print('Id not found')
        res = response['results']
        res_stat =  response['status']
        print(f'{res} {res_stat}')
    
def publish_message(topic_arn, message):
    sns_client = boto3.client('sns')
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
        )['MessageId']
    except ClientError:
        print(f'Could not publish message to the topic.')
        raise
    else:
        return response