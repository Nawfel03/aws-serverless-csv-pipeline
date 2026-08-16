import json
import urllib.parse
import boto3
import csv

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

TABLE_NAME = 'ProcessedData'
SNS_TOPIC_ARN = 'PASTE_YOUR_SNS_TOPIC_ARN_HERE'

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        lines = response['Body'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(lines)
        
        count = 0
        for row in reader:
            record_id = row.get('id') if row.get('id') else str(count)
            table.put_item(
                Item={
                    'FileId': key,
                    'RecordId': str(record_id),
                    'Name': str(row.get('name', 'N/A')),
                    'Value': str(row.get('value', '0'))
                }
            )
            count += 1
            
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Success! Processed {count} records from file '{key}'.",
            Subject="AWS Pipeline Alert: Success"
        )
        return {'statusCode': 200, 'body': 'File Processed Successfully'}
        
    except Exception as e:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Failed to process file '{key}'. Error: {str(e)}",
            Subject="AWS Pipeline Alert: Error"
        )
        raise e
