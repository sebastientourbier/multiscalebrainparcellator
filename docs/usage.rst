*********************
Usage
*********************

Execution and the BIDS format
=============================

The ``Multi-Scale Brain Parcellator`` workflow takes as principal input the path of the dataset
that is to be processed.
The input dataset is required to be in valid :abbr:`BIDS (Brain Imaging Data
Structure)` format, and it must include at least one T1w or MPRAGE structural image.
We highly recommend that you validate your dataset with the free, online
`BIDS Validator <http://bids-standard.github.io/bids-validator/>`_.

Commandline Arguments
=============================

The command to run ``Multi-Scale Brain Parcellator`` follow the `BIDS-Apps
<https://github.com/BIDS-Apps>`_ definition with additional options specific to this pipeline.

.. argparse::
		:ref: cmp.multiscalebrainparcellator.parser.get
		:prog: multiscalebrainparcellator


Participant Level Analysis
===========================
To run the docker image in participant level mode (for one participant)::

  docker run -it --rm \
  -v /home/localadmin/data/ds001:/bids_dataset \
  -v /media/localadmin/data/ds001/derivatives:/bids_dataset/derivatives \
  -v /usr/local/freesurfer/license.txt:/opt/freesurfer/license.txt \
  sebastientourbier/multiscalebrainparcellator:latest \
  /bids_dataset /bids_dataset/derivatives participant --participant_label 01 \
	--isotropic_resolution 1.0 \
	--thalamic_nuclei \
	--hippocampal_subfields \
	--brainstem_structures

.. note:: The local directory of the input BIDS dataset (here: ``/home/localadmin/data/ds001``) and the output directory (here: ``/media/localadmin/data/ds001/derivatives``) used to process have to be mapped to the folders ``/bids_dataset`` and ``/bids_dataset/derivatives`` respectively using the ``-v`` docker run option.


Debugging
=========

Logs are outputted into
``<output dir>/cmp/sub-<participant_label>/sub-<participant_label>_log-multiscalebrainparcellator.txt``.

Support and communication
=========================

The documentation of this project is found here: http://multiscalebrainparcellator.readthedocs.org/en/latest/.

All bugs, concerns and enhancement requests for this software can be submitted here:
https://github.com/sebastientourbier/multiscalebrainparcellator/issues.


If you run into any problems or have any questions, you can post to the `CMTK-users group <http://groups.google.com/group/cmtk-users>`_.


Not running on a local machine? - Data transfer
===============================================

If you intend to run ``multiscalebrainparcellator`` on a remote system, you will need to
make your data available within that system first. Comprehensive solutions such as `Datalad
<http://www.datalad.org/>`_ will handle data transfers with the appropriate
settings and commands. Datalad also performs version control over your data.
