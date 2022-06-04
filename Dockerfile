FROM golang:1.18-alpine as build

WORKDIR /src

COPY go.mod go.sum /src/

RUN go mod download

COPY ./ /src/

RUN CGO_ENABLED=0 go build -o /root/main cmd/main/main.go

FROM ubuntu:20.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /root/main /main

CMD /main