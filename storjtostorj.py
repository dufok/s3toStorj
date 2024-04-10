import boto3
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Make Working SetUp

storj_source = boto3.client(
    "s3",
    aws_access_key_id=os.environ["STORJ_SOURCE_ACCESS_KEY"],
    aws_secret_access_key=os.environ["STORJ_SOURCE_SECRET_KEY"],
    endpoint_url=os.environ["STORJ_SOURCE_END_POINT"],
)

storj_destination = boto3.client(
    "s3",
    aws_access_key_id=os.environ["STORJ_DESTINATION_ACCESS_KEY"],
    aws_secret_access_key=os.environ["STORJ_DESTINATION_SECRET_KEY"],
    endpoint_url=os.environ["STORJ_DESTINATION_END_POINT"],
)

source_bucket = os.environ["SOURCE_BUCKET"]
destination_bucket = os.environ["DESTINATION_BUCKET"]
logging.info(f"Source Bucket: {source_bucket}")
logging.info(f"Destination Bucket: {destination_bucket}")

paginator = storj_source.get_paginator("list_objects_v2")
pages = paginator.paginate(Bucket=source_bucket)

for page in pages:
    for obj in page["Contents"]:
        copy_source = {
            'Bucket': source_bucket,
            'Key': obj['Key']
        }
        storj_destination.copy(copy_source, destination_bucket, obj['Key'])
        logging.info(f"Copied {obj['Key']} from {source_bucket} to {destination_bucket}")