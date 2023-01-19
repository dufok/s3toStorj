# S3toStorjMIG
This is solution for migrating from S3 aws to Storj database

This is must be a solution for migrating. It is mean that you already have AWS S3 anf Storj accounts
with created access and permitions.

So you can add keys in Docker file like that:

`ARG S3_ACCESS_KEY=
ARG S3_SECRET_KEY=
ARG BUCKET=
ARG STORJ_ACCESS_KEY=
ARG STORJ_SECRET_KEY=
ARG STORJ_END_POINT=https://gateway.storjshare.io`

Or like Variable.

Don't forget to prepare you Storj bucket =)
