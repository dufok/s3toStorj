import boto3
import os
import tempfile
import difflib
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
                file.write(key['Key'] + "\n")
    logging.info(f'Creating list for bucket: {bucket}, filename: {filename}')

#  make list content of S3
list_creator(s3, bucket, '/output/s3_content.txt')
#  make list content of Storj
list_creator(storj, bucket, '/output/storj_content.txt')

# Compare two files
def compare(filename2, filename1, added_file, removed_file):
    with open(filename1) as file1, open(filename2) as file2, \
         open(added_file, 'w') as added_file_obj, open(removed_file, 'w') as removed_file_obj:
        file1 = file1.read()
        file2 = file2.read()
        difference = difflib.unified_diff(file1.splitlines(), file2.splitlines(), lineterm='', n=0)
        lines = list(difference)[2:]
        added = [line[1:] for line in lines if line[0] == '+' and not line.endswith("/")]
        removed = [line[1:] for line in lines if line[0] == '-' and not line.endswith("/")]
        for line in added:
            added_file_obj.writelines(line + '\n')
        for line in removed:
            removed_file_obj.writelines(line + '\n')
    logging.info(f'Comparing files: {filename1}, {filename2}')

compare('/output/s3_content.txt', '/output/storj_content.txt', '/output/diff_added.txt', '/output/diff_removed.txt')
print('diff creted')

if os.path.isfile('/output/diff_content.txt') and os.path.getsize('/output/diff_content.txt') > 0:
    print("Differences were written to /output/diff_content.txt")
else:
    logging.error("No differences found or failed to write the differences.")
    raise SystemExit


# Create a temporary directory
temp_dir = tempfile.TemporaryDirectory()

# Delete files from the storj S3 account
def delete_files(client, bucket, files):
    for file in files:
        try:
            client.delete_object(Bucket=bucket, Key=file)
            logging.info(f'{file} deleted from {bucket}')
        except Exception as e:
            logging.error(f'Failed to delete {file} from {bucket}: {e}')

# Read the list of files from the diff_removed.txt file
with open('/output/diff_removed.txt', 'r') as f:
    files_to_delete = f.read().splitlines()

delete_files(storj, bucket, files_to_delete)

# Read the list of files from the content.txt file
with open('/output/diff_added.txt', 'r') as f:
    files_to_add = f.read().splitlines()

for file_route in files_to_add:
    file_path = temp_dir.name + '/' + file_route
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    # Download the file from the first S3 account
    try:
        with open(file_path, 'wb') as f:
            s3.download_fileobj(
                Bucket=bucket,
                Key=file_route,
                Fileobj=f
            )
        logging.info(f'{file_route} downloaded from {bucket}')
    except Exception as e:
        logging.error(f'Failed to download {file_route} from {bucket}: {e}')

    # Upload the file to the second S3 account
    try:
        with open(file_path, 'rb') as f:
            storj.upload_fileobj(
                Fileobj=f,
                Bucket=bucket,
                Key=file_route
                )
        logging.info(f'{file_route} uploaded to {bucket}')
    except Exception as e:
        logging.error(f'Failed to upload {file_route} to {bucket}: {e}')
    temp_dir.cleanup()

# Delete the temporary directory
temp_dir.cleanup()
logging.info('Temporary directory deleted')

# Clen Up directory
files = os.listdir('/output')
logging.info('Cleaned up output directory')

# Iterate over the files
for file in files:
    # Construct the file path
    file_path = os.path.join('/output', file)
    # Check if the file is a file
    if os.path.isfile(file_path):
        # Remove the file
        os.remove(file_path)