#!/bin/sh

if [ "$1" = "-h" ] 
then
  echo "Usage: `basename $0` bids_dir output_dir participant_label"
  echo ""
  echo "	where:"
  echo "	- bids_dir : absolute path to your BIDS root directory"
  echo "	- output_dir : absolute path to your BIDS derivatives/output directory"
  echo "	- participant_label : a unique integer corresponding to the subject label"
  echo "	to be analyzed for the test"
  exit 0
fi

VERSION=$(python get_version.py)
echo $VERSION

docker run -v ${1}:/bids_dir \
-v ${2}:/output_dir \
-it sebastientourbier/multiscalebrainparcellator:$VERSION \
'/bids_dir' '/output_dir' \
participant --participant_label ${3} --skip_bids_validator