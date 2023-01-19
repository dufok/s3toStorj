FROM python:3.10
# add mount point
RUN mkdir ./output

# AWS S3 Keys
ARG S3_ACCESS_KEY=AKIAIWVLVZ334K4VP26Q
ARG S3_SECRET_KEY=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
ARG BUCKET=discours-io
# Storj Keys
ARG STORJ_ACCESS_KEY=jvmhhfjwzecz3ozl47gatcmjf7oa
ARG STORJ_SECRET_KEY=jycvsp2n5db6ngbuw6wsqudykxhoafm5drnhy5pkg4u3d4lycspyw
ARG STORJ_END_POINT=https://gateway.storjshare.io

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY migration.py ./
RUN python3 ./migration.py
