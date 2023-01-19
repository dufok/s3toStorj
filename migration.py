import boto3
from botocore.exceptions import ClientError
import os
import filecmp
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


# ---
#  make list content fof S3
with open("/output/s3_contex_new.txt", "a") as file:
    for key in s3.list_objects_v2(Bucket=bucket)['Contents']:
        file.write(key['Key'] + "\n")
print('file /output/s3_contex_new.txt is created')

# download file with old content from Storj 
try:
    storj.head_object(Bucket=bucket, Key='config/s3_contex_new.txt')
    storj.download_fileobj(
            Fileobj='output/s3_contex_old.txt',
            Bucket=bucket,
            Key='config/s3_contex_new.txt'
    )
    print('file config/s3_contex_new.txt downloaded')
except storj.exceptions.ClientError:
    open('output/s3_contex_old.txt', 'a').close()
    print('No file config/s3_contex_new.txt in BUCKET')
    print('file output/s3_contex_old.txt is created')


# Compare two files
# TEMPORARY change file1 and file2 
with open('/output/s3_contex_new.txt') as file1, open('/output/s3_contex_old.txt') as file2, open('/output/content.txt', 'w') as output_file:
    file1_contents = file1.read()
    file2_contents = file2.read()
    differences = list(difflib.context_diff(file1_contents.splitlines(), file2_contents.splitlines()))
    filtered_lines = [line[1:].lstrip() for line in differences if line.startswith("-") and not line.startswith("---")]
    output_file.writelines(line + '\n' for line in filtered_lines)

#  cheak work of difference metod
if os.path.isfile('/output/content.txt') and os.path.getsize('/output/content.txt') > 0:
   print("Differences were written to /output/content.txt")
else:
    print("No differences found or failed to write the differences.")
    raise SystemExit

# Read the list of files from the content.txt file
with open('/output/content.txt', 'r') as f:
    files_list = f.read().splitlines()
# Create a temporary directory
temp_dir = tempfile.TemporaryDirectory()

for file_route in files_list:
    directory = os.path.dirname(temp_dir.name + '/' + file_route)
    file_path = temp_dir.name + '/' + file_route
    if not os.path.exists(directory):
        if os.path.isfile(file_path):
            temp_name = file_path + ".temp"
            os.rename(file_path, temp_name)
            os.makedirs(directory)
            os.rename(temp_name, file_path)
        else:
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

# Delete the temporary directory
temp_dir.cleanup()

# upolad file with new content to Storj bucket config
storj.upload_file(
    Filename='output/s3_contex_new.txt',
    Bucket=bucket,
    Key='config/s3_contex_new.txt'
)

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