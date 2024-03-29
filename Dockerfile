FROM node:18-alpine as build

WORKDIR /src

COPY yarn.lock package.json /src/

RUN yarn install

COPY . /src/

RUN yarn build

FROM node:18-alpine as prod

# RUN apt-get update && \
#     apt-get upgrade -y && \
#     apt-get install -y tzdata && \
#     ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
#     dpkg-reconfigure -f noninteractive tzdata && \
#     rm -rf /var/lib/apt/lists/*

COPY --from=build /src/dist /src/package.json /src/yarn.lock /dist/

WORKDIR /dist

RUN yarn --production=true && rm /dist/package.json /dist/yarn.lock

CMD node index.js