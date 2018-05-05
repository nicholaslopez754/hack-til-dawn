import boto3
import config

"""
BUCKETS
"""
s3 = boto3.resource('s3',aws_access_key_id=config.aws_account_id,
                         aws_secret_access_key=config.aws_account_secret,
                         region_name='us-east-1')
train_bucket = 'crowdcam-training'
raw_bucket = 'crowdcam-raw'
match_butcket = 'crowdcam-matches'

"""
Rekognition
"""
client=boto3.client('rekognition',
    aws_access_key_id=config.aws_account_id,
    aws_secret_access_key=config.aws_account_secret,
    region_name='us-east-1')

response = client.detect_labels(Image=
    {
        'S3Object': {
            'Bucket': raw_bucket,
            'Name': 'image1.jpeg'
        }
    })

print(response)
