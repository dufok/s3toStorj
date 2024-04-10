# S3toStorjMIG
This is solution for migrating from S3 aws to Storj database

This is must be a solution for migrating. It is mean that you already have AWS S3 anf Storj accounts
with created access and permitions.

### s3tostorj take list of content in Bucket on S3 and the bucket with same name on Storj
### Compare it and download from S3 to Storj the difference 🌟

So you can add keys in Docker file like that:

ENV S3_ACCESS_KEY=🗝 \
ENV S3_SECRET_KEY=🗝 \
ENV BUCKET=🗝 \
ENV STORJ_ACCESS_KEY=🗝 \
ENV STORJ_SECRET_KEY=🗝 \
ENV STORJ_END_POINT=https://gateway.storjshare.io
or use ARG

If you use dokku then
dokku config:set $APP_NAME S3_ACCESS_KEY=🗝 S3_SECRET_KEY=🗝 STORJ_ACCESS_KEY=🗝 STORJ_ACCESS_KEY=🗝 STORJ_SECRET_KEY=🗝 STORJ_END_POINT=https://gateway.storjshare.io BUCKET=🗝

Or like Variable in Vercel



Don't forget to prepare you Storj bucket =)

### Added Gitea CI config file but i think it can be used for any CI


### Local development

```shell

mkdir .venv
python3.12 -m venv .venv
poetry env use .venv/bin/python3.12
poetry update
```


## storjtostorj.py 
## Storj Bucket Copy Script (Between Different Accounts)

This script is used to copy all objects from one Storj bucket to another, where each bucket is in a different Storj account. It uses the `boto3` library to interact with the Storj S3 compatible API.

### Environment Variables

The script requires the following variables:

- `STORJ_SOURCE_ACCESS_KEY`: Your source Storj account's access key.
- `STORJ_SOURCE_SECRET_KEY`: Your source Storj account's secret key.
- `STORJ_SOURCE_END_POINT`: The Storj endpoint URL for the source account. For example, `https://gateway.storjshare.io`.
- `STORJ_DESTINATION_ACCESS_KEY`: Your destination Storj account's access key.
- `STORJ_DESTINATION_SECRET_KEY`: Your destination Storj account's secret key.
- `STORJ_DESTINATION_END_POINT`: The Storj endpoint URL for the destination account.
- `SOURCE_BUCKET`: The name of the source bucket in the source Storj account.
- `DESTINATION_BUCKET`: The name of the destination bucket in the destination Storj account.

### How to Run

1. Set the required environment variables.
2. Run the script with Python 3.

```shell
python3 storjtostorj.py
```

### How it Works

The script first establishes a connection to both Storj accounts using the provided access keys, secret keys, and endpoint URLs. It then lists all objects in the source bucket and copies each one to the destination bucket.

The script logs each copy operation, so you can see the progress in the console.

Please note that the destination bucket should be empty before running the script to avoid overwriting existing objects.
