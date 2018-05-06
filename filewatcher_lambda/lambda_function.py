import recognize
import config
def lambda_handler(event, context):
    # TODO implement
   # result=recognize.index_from_raw(config.raw_collection)
    result=recognize.index_raw_image(event["Records"][0]["s3"]["object"]["key"], config.raw_collection)
    return result
