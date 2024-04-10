import boto3
import os
import tempfile
import logging
import json

from dotenv import load_dotenv
load_dotenv('.env')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Make Working SetUp

storj_source = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("STORJ_SOURCE_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("STORJ_SOURCE_SECRET_KEY"),
    endpoint_url=os.getenv("STORJ_SOURCE_END_POINT"),
)

storj_destination = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("STORJ_DESTINATION_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("STORJ_DESTINATION_SECRET_KEY"),
    endpoint_url=os.getenv("STORJ_DESTINATION_END_POINT"),
)

bucket = os.getenv("BUCKET")
logging.info(f"Bucket: {bucket}")


# Create a temporary directory
temp_dir = tempfile.TemporaryDirectory()

# Read the list of files from the content.txt file
with open("problem_files.txt", "r") as f:
    files_to_add = f.read().splitlines()

url_mapping = {}

for file_route in files_to_add:
    file_path = temp_dir.name + "/" + file_route
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

    # Download the file from the first S3 account
    try:
        with open(file_path, "wb") as f:
            storj_source.download_fileobj(Bucket=bucket, Key=file_route, Fileobj=f)
        logging.info(f"{file_route} downloaded from {bucket}")
    except Exception as e:
        logging.error(f"Failed to download {file_route} from {bucket}: {e}")

    # Upload the file to the second S3 account
    try:
        with open(file_path, "rb") as f:
            storj_destination.upload_fileobj(Fileobj=f, Bucket=bucket, Key=file_route)
        logging.info(f"{file_route} uploaded to {bucket}")

        # Update URL mapping
        url_mapping[file_route] = f"https://{bucket}.s3.amazonaws.com/{file_route}"

    except Exception as e:
        logging.error(f"Failed to upload {file_route} to {bucket}: {e}")
    temp_dir.cleanup()

# Write URL mapping to a JSON file
with open("/output/url_mapping.json", "w") as url_mapping_file:
    json.dump(url_mapping, url_mapping_file, indent=2)

logging.info("URL mapping created and uploaded")

# Delete the temporary directory
temp_dir.cleanup()
logging.info("Temporary directory deleted")

# Iterate over the files
for file in files_to_add:
    # Construct the file path
    file_path = os.path.join("/output", file)
    # Check if the file is a file
    if os.path.isfile(file_path):
        # Remove the file
        os.remove(file_path)
