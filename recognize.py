import boto3
import config

s3 = boto3.resource('s3',aws_access_key_id=config.aws_account_id,
                         aws_secret_access_key=config.aws_account_secret,
                         region_name='us-east-1')

#_photos_bucket = _s3.Bucket('crowdcam-bucket')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)