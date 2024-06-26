import boto3
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configure S3 and Storj clients
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["S3_ACCESS_KEY"],
    aws_secret_access_key=os.environ["S3_SECRET_KEY"],
)

storj = boto3.client(
    "s3",
    aws_access_key_id=os.environ["STORJ_ACCESS_KEY"],
    aws_secret_access_key=os.environ["STORJ_SECRET_KEY"],
    endpoint_url=os.environ["STORJ_END_POINT"],
)

bucket = os.environ["BUCKET"]
logging.info(f"Bucket: {bucket}")


def search_file(client, bucket, filename):
    try:
        # List objects with the specified prefix (file name)
        response = client.list_objects_v2(Bucket=bucket, Prefix=filename)
        # Check if the file exists
        if "Contents" in response and response["Contents"]:
            logging.info(f"{filename} found in {bucket}")
            return True
        else:
            logging.info(f"{filename} not found in {bucket}")
            return False
    except Exception as e:
        logging.error(f"Error searching for {filename} in {bucket}: {e}")
        return False


# Specify the name of the file you're searching for
filename = "production/audio/c40c9270-03bb-11ee-ac97-630f0de74335.mp3"

# Search for the file in both S3 and Storj
file_in_s3 = search_file(s3, bucket, filename)
file_in_storj = search_file(storj, bucket, filename)
