FROM python:3.12.3-bullseye AS builder-image

WORKDIR /app

ENV PY_BIN=python

RUN apt update && apt install -y git

# Compile google_crc32c for python3.12
# https://github.com/googleapis/python-crc32c/issues/178#issuecomment-2001053600
RUN git clone --recursive --depth 1 --branch v1.5.0 https://github.com/googleapis/python-crc32c \
    && cd python-crc32c  \
    && pip install -r scripts/dev-requirements.txt \
    && ./scripts/local-linux/build_libcrc32c.sh \
    && pip install --no-index --find-links=wheels google-crc32c \
    && python ./scripts/check_crc32c_extension.py \
    && python -c "from google_crc32c import *" \
    && ls --hide=usr | xargs -d '\n' rm -rf

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12.3-slim

WORKDIR /app

ENV PYTHONPATH=.

# Copy the built dependencies from the builder-image stage
COPY --from=builder-image /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY . .

# Copy libcrc32c.so shared library
COPY --from=builder-image /app/python-crc32c/usr/lib /app/python-crc32c/usr/lib

CMD ["python", "app.py"]
