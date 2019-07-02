# Copyright (C) 2017-2019, Brain Communication Pathways Sinergia Consortium, Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

ARG MAIN_DOCKER
FROM $MAIN_DOCKER

MAINTAINER Sebastien Tourbier <sebastien.tourbier@alumni.epfl.ch>

# Set the working directory to /app and copy contents of this repository
WORKDIR /app
ADD . /app

# Install multiscalebrainparcellator inside installed conda environment (see environment.yml)
ENV CONDA_ENV py27msbparc
RUN /bin/bash -c ". activate $CONDA_ENV && \
    python setup.py install"

ENV FS_LICENSE /bids_dir/code/license.txt

#COPY version /version
ENTRYPOINT ["multiscalebrainparcellator_bidsapp_entrypointscript"]

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="MULTISCALEBRAINPARCELLATOR" \
      org.label-schema.description="MULTISCALEBRAINPARCELLATOR - 5-scale brain parcellation tool" \
      org.label-schema.url="https://multiscalebrainparcellator.readthedocs.io" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/sebastientourbier/multiscalebrainparcellator" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"
