import boto3
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Make Working SetUp

s3 = boto3.client('s3',
                    aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                    aws_secret_access_key=os.environ['S3_SECRET_KEY'],
                     )

storj = boto3.client('s3',
                    aws_access_key_id=os.environ['STORJ_ACCESS_KEY'],
                    aws_secret_access_key=os.environ['STORJ_SECRET_KEY'],
                    endpoint_url=os.environ['STORJ_END_POINT']
                     )

bucket = os.environ['BUCKET']
logging.info(f'Bucket: {bucket}')

def list_creator(client, bucket, filename):
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket)

    with open(filename, "a") as file:
        for page in pages:
            for key in page['Contents']:
                file_path = key['Key']
                file.write(file_path + "\n")
    logging.info(f'Creating list for bucket: {bucket}, filename: {filename}')


#  make list content of S3
list_creator(s3, bucket, '/output/s3_content.txt')
#  make list content of Storj
list_creator(storj, bucket, '/output/storj_content.txt')

# Compare two files
def compare(filename2, filename1, added_file, removed_file):
    with open(filename1) as file1, open(filename2) as file2:
        file1_lines = set(file1.read().splitlines())
        file2_lines = set(file2.read().splitlines())

    added = file2_lines - file1_lines
    removed = file1_lines - file2_lines

    with open(added_file, 'w') as added_file_obj:
        for line in added:
            added_file_obj.writelines(line + '\n')

    with open(removed_file, 'w') as removed_file_obj:
        for line in removed:
            removed_file_obj.writelines(line + '\n')

    logging.info(f'Comparing files: {filename1}, {filename2}')

compare('/output/s3_content.txt', '/output/storj_content.txt', '/output/diff_added.txt', '/output/diff_removed.txt')
logging.info('diff created')


def search_file(client, bucket, filename):
    try:
        response = client.list_objects_v2(
            Bucket=bucket,
            Prefix=filename
        )
        logging.info(f'Response received: {response}')  # Log the entire response
        if 'Contents' in response and response['Contents']:
            logging.info(f'{filename} found in {bucket}')
            return True
        else:
            logging.info(f'{filename} not found in {bucket}')
            return False
    except Exception as e:
        logging.error(f'Error searching for {filename} in {bucket}: {e}')
        return False


# Read the list of added files
with open('/output/diff_added.txt', 'r') as f:
    files_to_find = f.read().splitlines()

# Try to find the first file that was added
if files_to_find:
    first_added_file = files_to_find[0]
    file_in_s3 = search_file(s3, bucket, first_added_file)
    file_in_storj = search_file(storj, bucket, first_added_file)
else:
    logging.info('No files were added.')