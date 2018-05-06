import boto3
import config

"""
BUCKETS
"""
s3 = boto3.resource('s3',
    aws_access_key_id=config.aws_account_id,
    aws_secret_access_key=config.aws_account_secret,
    region_name='us-east-1')

"""
Rekognition
"""
client = boto3.client('rekognition',
    aws_access_key_id=config.aws_account_id,
    aws_secret_access_key=config.aws_account_secret,
    region_name='us-east-1')

def get_user_images(user_id):
    bucket = s3.Bucket(config.train_bucket)
    prefix = '{}'.format(user_id)
    bucket_content = bucket.objects.filter(Prefix=prefix)
    return [obj.key for obj in bucket_content if '.jpeg' in obj.key]

def index_raw_image(image_name, collection):
    response = client.index_faces(
            CollectionId=collection,
            Image={
                'S3Object': {
                    'Bucket': config.raw_bucket,
                    'Name': image_name
                }
            },
            ExternalImageId=image_name
        )

def reset_collection(collection):
    cols = client.list_collections()['CollectionIds']
    if collection in cols:
        client.delete_collection(
            CollectionId=collection
        )
    client.create_collection(
            CollectionId=collection
    )

# Testing utility function to simulate lambda index
def index_from_raw(collection):
    # Make a fresh collection
    reset_collection(collection)

    # Index every image from the raw bucket
    bucket = s3.Bucket(config.raw_bucket)
    for obj in bucket.objects.all():
        client.index_faces(
            CollectionId=collection,
            Image={
                'S3Object': {
                    'Bucket': config.raw_bucket,
                    'Name': obj.key
                }
            },
            ExternalImageId=obj.key
        )

def search_collection(input_img, collection, threshold):
    return client.search_faces_by_image(
        CollectionId=collection,
        Image={
            'S3Object': input_img
        },
        MaxFaces=100,
        FaceMatchThreshold=threshold
    )

def create_train_image(name):
    return {
        'Bucket': config.train_bucket,
        'Name': name
    }