FROM python:3.10
# add mount point
RUN mkdir ./output
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY s3tostorj.py ./
COPY find.py ./
COPY test.py ./
# For testing and find files in the bucket use find.py
CMD [ "python3", "s3tostorj.py"]