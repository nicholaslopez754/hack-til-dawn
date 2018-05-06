import boto3
import config

"""
BUCKETS
"""
s3 = boto3.resource('s3',
    aws_access_key_id=config.aws_account_id,
    aws_secret_access_key=config.aws_account_secret,
    region_name='us-east-1')

train_bucket = 'crowdcam-training'
raw_bucket = 'crowdcam-raw'
match_butcket = 'crowdcam-matches'

"""
Rekognition
"""
client = boto3.client('rekognition',
    aws_access_key_id=config.aws_account_id,
    aws_secret_access_key=config.aws_account_secret,
    region_name='us-east-1')

def get_imgs_from_id(user_id):
    bucket = s3.Bucket(train_bucket)
    prefix = '{}'.format(user_id)
    bucket_content = bucket.objects.filter(Prefix=prefix)
    return [obj.key for obj in bucket_content if '.jpeg' in obj.key]

def simulate_stream_index():
    frames = [
        {
            'S3Object': {
                'Bucket': raw_bucket,
                'Name': 'image1.jpeg'
            }
        },
        {
            'S3Object': {
                'Bucket': raw_bucket,
                'Name': 'image2.jpeg'
            }
        },
        {
            'S3Object': {
                'Bucket': raw_bucket,
                'Name': 'image3.jpeg'
            }
        },
        {
            'S3Object': {
                'Bucket': raw_bucket,
                'Name': 'image5.jpeg'
            }
        }
    ]

    for frame in frames:
        response = client.index_faces(
            CollectionId='test_collection',
            Image={
                'S3Object': frame['S3Object']
            },
            ExternalImageId=frame['S3Object']['Name']
        )
        print(response)

def search_collection(input_img, collection):
    return client.search_faces_by_image(
        CollectionId=collection,
        Image={
            'S3Object': input_img
        },
        MaxFaces=100,
        FaceMatchThreshold=1
    )

if __name__ == '__main__':
    test_img = {
        'Bucket': train_bucket,
        'Name': get_imgs_from_id('2D2BB700-419A-4BC0-B2F0-8C54D0A6D6A0')[0]
    }
    print(test_img)
    collection = 'test_collection'

    print(search_collection(test_img, collection)['FaceMatches'])