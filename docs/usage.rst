*********************
Usage
*********************

Execution and the BIDS format
=============================

The ``Multi-Scale Brain Parcellator`` workflow takes as principal input the path of the dataset
that is to be processed.

The input dataset is required to be in valid :abbr:`BIDS (Brain Imaging Data
Structure)` format, and it must include at least one T1w or MPRAGE structural image. For example::

    ds-example/
    	
    	README
    	CHANGES
    	participants.tsv
    	dataset_description.json
        
        sub-01/
            anat/
            	sub-01_T1w.nii.gz
            	sub-01_T1w.json
        
        ...

        sub-<subject_label>/
            anat/
            	sub-<subject_label>_T1w.nii.gz
            	sub-<subject_label>_T1w.json
            ...
        ...

For more information about BIDS, please consult the `BIDS Website <https://bids.neuroimaging.io/>`_ and the `Online BIDS Specifications <https://bids-specification.readthedocs.io/en/stable/>`_. `HeuDiConv <https://github.com/nipy/heudiconv>`_ can assist you in converting DICOM brain imaging data to BIDS. A nice tutorial can be found @ `BIDS Tutorial Series: HeuDiConv Walkthrough <http://reproducibility.stanford.edu/bids-tutorial-series-part-2a/>`_ .

.. important:: 
	We highly recommend that you validate your dataset with the free, online `BIDS Validator <http://bids-standard.github.io/bids-validator/>`_.


Commandline Arguments
=============================

The command to run ``Multi-Scale Brain Parcellator`` follow the `BIDS-Apps
<https://github.com/BIDS-Apps>`_ definition with additional options specific to this pipeline.

.. argparse::
		:ref: cmp.multiscalebrainparcellator.parser.get
		:prog: multiscalebrainparcellator

.. seealso:: 
	More information about BIDS Apps? Please check directly on the `BIDS Apps Website <http://bids-apps.neuroimaging.io/>`_.


Participant Level Analysis
===========================

To run the docker image in participant level mode (for one participant):

.. code-block:: bash
  
    $ docker run -it --rm \
    -v /home/localadmin/data/ds-example:/bids_dir \
    -v /media/localadmin/data/ds-example/derivatives:/output_dir \
    -v /usr/local/freesurfer/license.txt:/bids_dir/code/license.txt \
    sebastientourbier/multiscalebrainparcellator:v1.1.0 \
    /bids_dir /output_dir participant --participant_label 01 \
    --isotropic_resolution 1.0 \
    --thalamic_nuclei \
    --hippocampal_subfields \
    --brainstem_structures

.. important:: The local directory of the input BIDS dataset (here: ``/home/localadmin/data/ds001``) and the output directory (here: ``/media/localadmin/data/ds001/derivatives``) used to process have to be mapped to the folders ``/bids_dir`` and ``/output_dir`` respectively using the ``-v`` docker run option.

.. important:: **Multi-scale brain parcellator needs your own Freesurfer license**. As a result, you must map your license (for instance ``/usr/local/freesurfer/license.txt``) to the file ``/bids_dir/code/license.txt`` inside the BIDS App.


Debugging
=========

Logs are outputted to ``sub-<participant_label>_log-multiscalebrainparcellator.txt`` located in ``<output dir>/cmp/sub-<participant_label>/`` directory.

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
