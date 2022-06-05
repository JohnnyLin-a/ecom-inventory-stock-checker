FROM node:18-bullseye-slim as build

WORKDIR /src

COPY yarn.lock package.json /src/

RUN yarn install

COPY . /src/

RUN yarn build

FROM node:18-bullseye-slim as prod

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /src/dist /src/yarn.lock /src/package.json /dist/

WORKDIR /dist

RUN yarn --production=true

CMD node index.js