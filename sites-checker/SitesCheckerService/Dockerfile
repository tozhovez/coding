FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    zip \
    unzip \
    git-core && \
    python -m pip install --upgrade pip

COPY ./requirements.txt ./
RUN python -m pip install --user -r requirements.txt

ARG PUID=1000
ARG BUILD_VERSION
ENV VERSION=$BUILD_VERSION
ENV PATH=/root/.local/bin:$PATH
COPY . /app
WORKDIR /app

CMD ["python", "./main.py"]
