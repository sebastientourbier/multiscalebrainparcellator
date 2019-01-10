*********************
Outputs of Multi-Scale Brain Parcellator
*********************

.. note:: Multi-Scale Brain Parcellator outputs are currently being updated to conform to the :abbr:`BIDS (brain imaging data structure)` Common Derivatives specification (see `BIDS Common Derivatives Extension <https://docs.google.com/document/d/1Wwc4A6Mow4ZPPszDIWfCUCRNstn7d_zzaWPcfcHmgI4/edit>`_).

Multi-Scale Brain Parcellator Derivatives
==============

Processed, or derivative, data are written to ``<bids_dataset/derivatives>/cmp/sub-<subject_label>/``. In this folder, a configuration file generated and used for processing each participant is saved as ``sub-<subject_label>_anatomical_config.ini``

Anatomical derivatives in the original ``T1w`` space are placed in each subject's ``anat`` subfolder including:

- ``anat/sub-<subject_label>_T1w_space-orig_desc-head.nii.gz``
- ``anat/sub-<subject_label>_T1w_space-orig_desc-brain.nii.gz``
- ``anat/sub-<subject_label>_T1w_space-orig_desc-brain_mask.nii.gz``

- ``anat/sub-<subject_label>_T1w_space-orig_label-WM_dseg.nii.gz``
- ``anat/sub-<subject_label>_T1w_space-orig_label-GM_dseg.nii.gz``
- ``anat/sub-<subject_label>_T1w_space-orig_label-CSF_dseg.nii.gz``

The five different brain parcellation are saved as:

- ``anat/sub-<subject_label>_T1w_space-orig_label-L2018_desc-<scale_label>_atlas.nii.gz``

where ``<scale_label>`` : ``scale1``, ``scale2``, ``scale3``, ``scale4``, ``scale5`` corresponds to the parcellation scale.

Additionally, the description of parcel labels and the updated FreeSurfer color lookup table are saved:

- ``anat/sub-<subject_label>_T1w_space-orig_label-L2018_desc-<scale_label>_atlas.graphml``
- ``anat/sub-<subject_label>_T1w_space-orig_label-L2018_desc-<scale_label>_atlas_FreeSurferColorLUT.txt``


FreeSurfer Derivatives
------------

A FreeSurfer subjects directory is created in ``<bids_dataset/derivatives>/freesurfer``.

::

    freesurfer/
        fsaverage/
            mri/
            surf/
            ...
        sub-<subject_label>/
            mri/
            surf/
            ...
        ...

The ``fsaverage`` subject distributed with the running version of
FreeSurfer is copied into this directory.
