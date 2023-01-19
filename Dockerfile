FROM python:3.10
# add mount point
RUN mkdir ./output

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY migration.py ./
RUN python3 ./migration.py
