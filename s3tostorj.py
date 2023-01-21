import boto3
import os
import tempfile
import difflib

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


def list_creator(client, bucket, filename):
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket)

    with open(filename, "a") as file:
        for page in pages:
            for key in page['Contents']:
                file.write(key['Key'] + "\n")

#  make list content of S3
list_creator(s3, bucket, '/output/s3_content.txt')
#  make list content of Storj
list_creator(storj, bucket, '/output/storj_content.txt')

# Compare two files
def compare(filename2, filename1, outputfile):
    with open(filename1) as file1, open(filename2) as file2, open(outputfile, 'w') as output_file:
        file1 = file1.read()
        file2 = file2.read()
        difference = difflib.unified_diff(file1.splitlines(), file2.splitlines(), lineterm='', n=0)
        lines = list(difference)[2:]
        added = [line[1:] for line in lines if line[0] == '+' and not line.endswith("/")]
        removed = [line[1:] for line in lines if line[0] == '-' and not line.endswith("/")]
        for line in added:
            if line not in removed:
                output_file.writelines(line + '\n')

compare('/output/s3_content.txt', '/output/storj_content.txt', '/output/diff_content.txt')
print('diff creted')

if os.path.isfile('/output/diff_content.txt') and os.path.getsize('/output/diff_content.txt') > 0:
    print("Differences were written to /output/diff_content.txt")
else:
    print("No differences found or failed to write the differences.")
    raise SystemExit


# Create a temporary directory
temp_dir = tempfile.TemporaryDirectory()

# Read the list of files from the content.txt file
with open('/output/diff_content.txt', 'r') as f:
    files_list = f.read().splitlines()

for file_route in files_list:
    file_path = temp_dir.name + '/' + file_route
    directory = os.path.dirname(temp_dir.name + '/' + file_route)
    os.makedirs(directory)
    # Download the file from the first S3 account
    with open(file_path, 'wb') as f:
        s3.download_fileobj(
            Bucket=bucket,
            Key=file_route,
            Fileobj=f
        )
    print(f'{file_route} downloaded from {bucket}')

    # Upload the file to the second S3 account
    with open(file_path, 'rb') as f:
        storj.upload_fileobj(
            Fileobj=f,
            Bucket=bucket,
            Key=file_route
            )
    print(f'{file_route} uploaded to {bucket}')
    temp_dir.cleanup()

# Delete the temporary directory
temp_dir.cleanup()

# Clen Up directory
files = os.listdir('/output')

# Iterate over the files
for file in files:
    # Construct the file path
    file_path = os.path.join('/output', file)
    # Check if the file is a file
    if os.path.isfile(file_path):
        # Remove the file
        os.remove(file_path)