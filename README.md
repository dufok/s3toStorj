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
