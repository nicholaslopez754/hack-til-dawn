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

def get_user_images(user_id):
    bucket = s3.Bucket(train_bucket)
    prefix = '{}'.format(user_id)
    bucket_content = bucket.objects.filter(Prefix=prefix)
    return [obj.key for obj in bucket_content if '.jpeg' in obj.key]

# Testing utility function to simulate lambda index
def index_from_raw():
    # Collection management
    cols = client.list_collections()['CollectionIds']
    if 'test_collection' in cols:
        client.delete_collection(
            CollectionId='test_collection'
        )
    client.create_collection(
            CollectionId='test_collection'
    )

    # Index every image from the raw bucket
    bucket = s3.Bucket(raw_bucket)
    for obj in bucket.objects.all():
        print(obj.key)
        client.index_faces(
            CollectionId='test_collection',
            Image={
                'S3Object': {
                    'Bucket': raw_bucket,
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

if __name__ == '__main__':
    test_img = {
        'Bucket': train_bucket,
        'Name': get_imgs_from_id('2D2BB700-419A-4BC0-B2F0-8C54D0A6D6A0')[0]
    }
    print(test_img)
    collection = 'test_collection'

    results = search_collection(test_img, collection, 70)['FaceMatches']
    for result in results:
        print(result['Face']['ExternalImageId'], result['Similarity'], sep='\t')
    #ndex_from_raw()