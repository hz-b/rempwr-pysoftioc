FROM ubuntu:20.04

ENV http_proxy http://www.bessy.de:3128
ENV https_proxy http://www.bessy.de:3128
ENV LD_LIBRARY_PATH=/usr/local/lib

RUN apt-get update \
&& apt-get -y install sudo \
&& apt-get -y install apt-utils  \
&& apt-get -y install dialog \
&& apt-get -y install python3.8 \
&& apt-get -y install python3-pip

# Set user and group
ARG user=docker
ARG group=docker
ARG uid=1002
ARG gid=1002
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} # <--- the '-m' create a user home directory
WORKDIR /home/docker
# Copy in the ipython directory and other dependencies

COPY /ioc /home/docker/ioc
RUN ls *

# Install all required python packages
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /home/docker/ioc/requirements.txt

USER docker
WORKDIR /home/docker/ioc

RUN ["python3", "./remote_power_ioc.py"]



