FROM node:18-bullseye-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN yarn global add ts-node

WORKDIR /src

COPY yarn.lock package.json /src/

RUN yarn install --production=true

COPY ./* /src/

RUN ts-node index.ts