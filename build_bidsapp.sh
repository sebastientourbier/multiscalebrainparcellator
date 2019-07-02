#! /bin/sh

CMP_BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo $CMP_BUILD_DATE

VERSION=$(python get_version.py)
echo $VERSION

VCS_REF=$(git rev-parse --verify HEAD)
echo $VCS_REF

MAIN_DOCKER=sebastientourbier/multiscalebrainparcellator-ubuntu16.04:$VERSION
#MAIN_DOCKER="sebastientourbier/multiscalebrainparcellator-ubuntu16.04:latest"
echo $MAIN_DOCKER

cd ubuntu16.04
docker build --rm --build-arg BUILD_DATE=$CMP_BUILD_DATE --build-arg VERSION=$VERSION --build-arg VCS_REF=$VCS_REF -t sebastientourbier/multiscalebrainparcellator-ubuntu16.04:${VERSION} .

cd ..
docker build --no-cache --rm --build-arg BUILD_DATE=$CMP_BUILD_DATE \
                             --build-arg VERSION=$VERSION \
                             --build-arg VCS_REF=$VCS_REF \
                             --build-arg MAIN_DOCKER=$MAIN_DOCKER \
                             -t sebastientourbier/multiscalebrainparcellator:${VERSION} .
