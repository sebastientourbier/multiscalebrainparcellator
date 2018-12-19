# Copyright (C) 2017-2019, Brain Communication Pathways Sinergia Consortium, Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

FROM sebastientourbier/multiscalebrainparcellator-ubuntu16.04:latest

MAINTAINER Sebastien Tourbier <sebastien.tourbier@alumni.epfl.ch>

# Set the working directory to /app and copy contents of this repository
WORKDIR /app
ADD . /app

#Clone the master branch of multiscalebrainparcellator from BitBucket
#RUN apt-get -qq -y install git-core
#RUN git clone --progress --verbose -b master --single-branch https://github.com/sebastientourbier/multiscalebrainparcellator.git multiscalebrainparcellator

# Set the working directory to /app/multiscalebrainparcellator and install multiscalebrainparcellator
WORKDIR /app
RUN python setup.py install

#COPY version /version
ENTRYPOINT ["multiscalebrainparcellator_bidsapp_entrypointscript"]
