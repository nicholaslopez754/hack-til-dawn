import boto3
import config

s3 = boto3.resource('s3',aws_access_key_id=config.aws_account_id,
                         aws_secret_access_key=config.aws_account_secret,
                         region_name='us-east-1')

train_bucket = s3.Bucket('crowdcam-training')
raw_bucket = s3.Bucket('crowdcam-raw')
match_butcket = s3.Bucket('crowdcam-matches')

