import boto3
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Make Working SetUp

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

# Clean up the output directory
def clean_output_directory(directory):
    if os.path.exists(directory):
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        logging.info("Cleaned up output directory")
    else:
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")

def list_creator(client, bucket, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    paginator = client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket)

    with open(filename, "a") as file:
        for page in pages:
            for key in page["Contents"]:
                file.write(key["Key"] + "\n")
    logging.info(f"Creating list for bucket: {bucket}, filename: {filename}")

# Call the function at the beginning of your script
clean_output_directory("/output")
#  make list content of S3
list_creator(s3, bucket, "/output/s3_content.txt")
#  make list content of Storj
list_creator(storj, bucket, "/output/storj_content.txt")


# Compare two files
def compare(filename2, filename1, diff_file):
    with open(filename1) as file1, open(filename2) as file2:
        file1_lines = set(file1.read().splitlines())
        file2_lines = set(file2.read().splitlines())

    diff = file2_lines - file1_lines

    with open(diff_file, "w") as diff_file_obj:
        for line in diff:
            diff_file_obj.writelines(line + "\n")

    logging.info(f"Comparing files: {filename1}, {filename2}")


compare("/output/s3_content.txt", "/output/storj_content.txt", "/output/diff.txt")
logging.info("diff created")