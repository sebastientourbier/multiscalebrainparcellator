# Use Ubuntu 16.04 LTS
FROM ubuntu:16.04

# Pre-cache neurodebian key
COPY files/neurodebian.gpg /root/.neurodebian.gpg

MAINTAINER Sebastien Tourbier <sebastien.tourbier@alumni.epfl.ch>

## Install miniconda2 and multiscalebrainparcellator dependencies including exfat libraries for exfat-formatted hard-drives (only MAC?)
RUN apt-get update && apt-get -qq -y install npm curl bzip2 exfat-fuse exfat-utils&& \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get update && apt-get -qq -y install nodejs && \
    npm install -g bids-validator && \
    curl -sSL http://neuro.debian.net/lists/xenial.us-ca.full >> /etc/apt/sources.list.d/neurodebian.sources.list && \
    apt-key add /root/.neurodebian.gpg && \
    (apt-key adv --refresh-keys --keyserver hkp://ha.pool.sks-keyservers.net 0xA5D32F012649A5A9 || true) && \
    curl -sSL https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -o /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -bfp /opt/conda && \
    rm -rf /tmp/miniconda.sh

ENV PATH /opt/conda/bin:$PATH

# Pull the environment name out of the environment.yml
ENV CONDA_ENV py27msbparc
ADD environment.yml /app/environment.yml
RUN conda env create -f /app/environment.yml && conda clean --all --yes

#Make ANTs happy
ENV ANTSPATH /opt/conda/envs/$CONDA_ENV/bin
ENV PATH $ANTSPATH:$PATH


# Installing Freesurfer
RUN curl -sSL https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/6.0.1/freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.1.tar.gz | tar zxv --no-same-owner -C /opt \
    --exclude='freesurfer/trctrain' \
    --exclude='freesurfer/subjects/fsaverage_sym' \
    --exclude='freesurfer/subjects/fsaverage3' \
    --exclude='freesurfer/subjects/fsaverage4' \
    --exclude='freesurfer/subjects/cvs_avg35' \
    --exclude='freesurfer/subjects/cvs_avg35_inMNI152' \
    --exclude='freesurfer/subjects/bert' \
    --exclude='freesurfer/subjects/V1_average' \
    --exclude='freesurfer/average/mult-comp-cor' \
    --exclude='freesurfer/lib/cuda' \
    --exclude='freesurfer/lib/qt'

# Installing the Matlab R2012b (v8.0) runtime
# Required by the brainstem and hippocampal subfield modules in FreeSurfer 6.0.1
WORKDIR /opt/freesurfer
RUN curl "http://surfer.nmr.mgh.harvard.edu/fswiki/MatlabRuntime?action=AttachFile&do=get&target=runtime2012bLinux.tar.gz" -o "runtime2012b.tar.gz"
RUN tar xvf runtime2012b.tar.gz
RUN rm runtime2012b.tar.gz

# Make Matlab runtime environment happy
RUN apt-get install -y -qq libxt6 libxmu-dev

# Make FreeSurfer happy
RUN apt-get install -y -qq tcsh bc

ENV FSL_DIR=/usr/share/fsl/5.0 \
    OS=Linux \
    FS_OVERRIDE=0 \
    FIX_VERTEX_AREA= \
    FSF_OUTPUT_FORMAT=nii.gz \
    FREESURFER_HOME=/opt/freesurfer
ENV SUBJECTS_DIR=$FREESURFER_HOME/subjects \
    FUNCTIONALS_DIR=$FREESURFER_HOME/sessions \
    MNI_DIR=$FREESURFER_HOME/mni \
    LOCAL_DIR=$FREESURFER_HOME/local \
    FSFAST_HOME=$FREESURFER_HOME/fsfast \
    MINC_BIN_DIR=$FREESURFER_HOME/mni/bin \
    MINC_LIB_DIR=$FREESURFER_HOME/mni/lib \
    MNI_DATAPATH=$FREESURFER_HOME/mni/data \
    FMRI_ANALYSIS_DIR=$FREESURFER_HOME/fsfast
ENV PERL5LIB=$MINC_LIB_DIR/perl5/5.8.5 \
    MNI_PERL5LIB=$MINC_LIB_DIR/perl5/5.8.5 \
    PATH=$FREESURFER_HOME/bin:$FSFAST_HOME/bin:$FREESURFER_HOME/tktools:$MINC_BIN_DIR:$PATH

# Installing Neurodebian packages (FSL)
RUN apt-get update && \
    apt-get install -y --no-install-recommends fsl-core=5.0.9-5~nd16.04+1

#Make FSL happy
ENV FSLDIR=/usr/share/fsl/5.0 \
    FSLOUTPUTTYPE=NIFTI_GZ \
    FSLMULTIFILEQUIT=TRUE \
    POSSUMDIR=/usr/share/fsl/5.0 \
    LD_LIBRARY_PATH=/usr/lib/fsl/5.0:$LD_LIBRARY_PATH \
    FSLTCLSH=/usr/bin/tclsh \
    FSLWISH=/usr/bin/wish

ENV PATH=/usr/lib/fsl/5.0:$PATH

# Add fsaverage
WORKDIR /opt/freesurfer/subjects/fsaverage
ADD . /bids_dir/derivatives/freesurfer/fsaverage

WORKDIR /

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="MULTISCALEBRAINPARCELLATOR SYSTEM IMAGE" \
      org.label-schema.description="Parent image of the multiscalebrainparcellator that provides a ubuntu 16.04 Xenial system with all prerequisites installed" \
      org.label-schema.url="https://multiscalebrainparcellator.readthedocs.io" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/sebastientourbier/multiscalebrainparcellator/environments" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"
