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


Usage
=============================

The command to run ``Multi-Scale Brain Parcellator`` follow the `BIDS-Apps
<https://github.com/BIDS-Apps>`_ definition with additional options specific to this pipeline::

        $ docker -ti --rm sebastientourbier/multiscalebrainparcellator --help

        usage: multiscalebrainparcellator_bidsapp_entrypointscript [-h]
                                        [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
																				[--isotropic_resolution RESOLUTION_IN_MM]
                                        [--thalamic_nuclei]
                                        [--hippocampal_subfields]
                                        [--brainstem_structures]
                                        [-v]
                                        bids_dir output_dir {participant,group}

        Multi-scale Brain Parcellator BIDS App entrypoint script.

        positional arguments:
          bids_dir              The directory with the input dataset formatted
                                according to the BIDS standard.
          output_dir            The directory where the output files should be stored.
                                If you are running group level analysis this folder
                                should be prepopulated with the results of
                                theparticipant level analysis.
          {participant,group}   Level of the analysis that will be performed. Multiple
                                participant level analyses can be run independently
                                (in parallel) using the same output_dir.

        optional arguments:
          -h, --help            show this help message and exit
          --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
                                The label(s) of the participant(s) that should be
                                analyzed. The label corresponds to
                                sub-<participant_label> from the BIDS spec (so it does
                                not include "sub-"). If this parameter is not provided
                                all subjects should be analyzed. Multiple participants
                                can be specified with a space separated list.
					--isotropic_resolution RESOLUTION_IN_MM
																The isotropic resolution in mm used to resample the
																original anatomical images and applied at the
																beginning of the processing pipeline.
          --thalamic_nuclei     Segment thalamic thalamic_nuclei
          --hippocampal_subfields Segment hippocampal subfields (FreeSurfer)
          --brainstem_structures Segment brainstem structures (FreeSurfer)
          -v, --version         show program's version number and exit

Participant level
======================
To run it in participant level mode (for one participant)::

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
