FROM ubuntu:20.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip firefox firefox-geckodriver && \
    pip3 install -U pip && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /root/requirements.txt

RUN pip3 install wheel setuptools && pip3 install -r /root/requirements.txt

VOLUME [ "/src" ]

CMD python3 -m cmd.main