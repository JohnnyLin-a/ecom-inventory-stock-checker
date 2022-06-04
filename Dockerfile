FROM node:18-bullseye-slim as build

WORKDIR /src

COPY yarn.lock package.json /src/

RUN yarn install --production=true

COPY . /src/

RUN yarn build

FROM node:18-bullseye-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /src/dist /dist/

WORKDIR /dist

CMD node index.js