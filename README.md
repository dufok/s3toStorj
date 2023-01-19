# S3toStorjMIG
This is solution for migrating from S3 aws to Storj database

This is must be a solution for migrating. It is mean that you already have AWS S3 anf Storj accounts
with created access and permitions.

So you can add keys in Docker file like that:

ARG S3_ACCESS_KEY=🗝 \
ARG S3_SECRET_KEY=🗝 \
ARG BUCKET=🗝 \
ARG STORJ_ACCESS_KEY=🗝 \
ARG STORJ_SECRET_KEY=🗝 \
ARG STORJ_END_POINT=https://gateway.storjshare.io \

If you use dokku then
dokku config:set $APP_NAME S3_ACCESS_KEY=🗝 S3_SECRET_KEY=🗝 STORJ_ACCESS_KEY=🗝 STORJ_ACCESS_KEY=🗝 STORJ_SECRET_KEY=🗝 STORJ_END_POINT=https://gateway.storjshare.io BUCKET=🗝

Or like Variable in Vercel

Don't forget to prepare you Storj bucket =)
