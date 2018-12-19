## Multi-Scale Brain Parcellator
This pipeline is developed by the Hagmann’s group at the University Hospital of Lausanne (CHUV) for use within the SNF Sinergia Project 170873 (![project website](https://sinergiaconsortium.bitbucket.io/)), as well as for open-source software distribution.

[![DockerAutomatedBuild](https://img.shields.io/docker/build/sebastientourbier/multiscalebrainparcellator.svg)](https://cloud.docker.com/repository/docker/sebastientourbier/multiscalebrainparcellator)
[![CircleCI](https://circleci.com/gh/sebastientourbier/multiscalebrainparcellator/tree/master.svg?style=shield)](https://circleci.com/gh/sebastientourbier/multiscalebrainparcellator/tree/master)

### About
The Multi-Scale Brain Parcellator is a BIDS App that implements a full anatomical MRI processing pipeline interfacing with FreeSurfer 6.0.1, FSLMATHS (FSL 5.0.9), ANTs 2.2.0 and the Connectome Mapping Toolkit (CMTK), from raw T1w data to structural brain parcellation at five different scales.


![Image not found](images/multiscalebrainparcellator_888x551.png)

### License
This software is distributed under the open-source license Modified BSD. See [license](LICENSE) for more details.

### Aknowledgments

If your are using the Multi-Scale Brain Parcellator in your work, please acknowledge this software and its dependencies. To do so, we recommend you to use, modify to your needs, and include in your work the following acknowledgment text:

> Results included in this manuscript come from the Multi-Scale Brain Parcellator version latest [1], a processing pipeline, written in Python which uses Nipype [2,3]. It is encapsulated in a BIDS app [4] based on Docker [5] and Singularity [6] container technologies. Resampling to isotropic resolution, Desikan-Killiany brain parcellation [7], brainstem parcellation [8], and hippocampal subfields segmentation [9] were performed using FreeSurfer 6.0.1. Final parcellations were created by performing cortical brain parcellation on at 5 different scales [10], probabilistic atlas-based segmentation of the thalamic nuclei [11],and combination of all segmented structures, using CMTK v3.0.0 [12] and the antsRegistrationSyNQuick of ANTS v2.2.0 [13].

#### References

1.Multi-Scale Brain Parcellator available from: doi:xx.YYYY/zenodo.ZZZZZZ.

2.Gorgolewski K, Burns CD, Madison C, Clark D, Halchenko YO, Waskom ML, Ghosh SS. Nipype: a flexible, lightweight and extensible neuroimaging data processing framework in python. Front Neuroinform. 2011 Aug 22;5(August):13. doi:10.3389/fninf.2011.00013. 

3.Gorgolewski KJ, Esteban O, Ellis DG, Notter MP, Ziegler E, Johnson H, Hamalainen C, Yvernault B, Burns C, Manhães-Savio A, Jarecka D, Markiewicz CJ, Salo T, Clark D, Waskom M, Wong J, Modat M, Dewey BE, Clark MG, Dayan M, Loney F, Madison C, Gramfort A, Keshavan A, Berleant S, Pinsard B, Goncalves M, Clark D, Cipollini B, Varoquaux G, Wassermann D, Rokem A, Halchenko YO, Forbes J, Moloney B, Malone IB, Hanke M, Mordom D, Buchanan C, Pauli WM, Huntenburg JM, Horea C, Schwartz Y, Tungaraza R, Iqbal S, Kleesiek J, Sikka S, Frohlich C, Kent J, Perez-Guevara M, Watanabe A, Welch D, Cumba C, Ginsburg D, Eshaghi A, Kastman E, Bougacha S, Blair R, Acland B, Gillman A, Schaefer A, Nichols BN, Giavasis S, Erickson D, Correa C, Ghayoor A, Küttner R, Haselgrove C, Zhou D, Craddock RC, Haehn D, Lampe L, Millman J, Lai J, Renfro M, Liu S, Stadler J, Glatard T, Kahn AE, Kong X-Z, Triplett W, Park A, McDermottroe C, Hallquist M, Poldrack R, Perkins LN, Noel M, Gerhard S, Salvatore J, Mertz F, Broderick W, Inati S, Hinds O, Brett M, Durnez J, Tambini A, Rothmei S, Andberg SK, Cooper G, Marina A, Mattfeld A, Urchs S, Sharp P, Matsubara K, Geisler D, Cheung B, Floren A, Nickson T, Pannetier N, Weinstein A, Dubois M, Arias J, Tarbert C, Schlamp K, Jordan K, Liem F, Saase V, Harms R, Khanuja R, Podranski K, Flandin G, Papadopoulos Orfanos D, Schwabacher I, McNamee D, Falkiewicz M, Pellman J, Linkersdörfer J, Varada J, Pérez-García F, Davison A, Shachnev D, Ghosh S. Nipype: a flexible, lightweight and extensible neuroimaging data processing framework in Python. 2017. doi:10.5281/zenodo.581704. 

4.Gorgolewski KJ, Alfaro-Almagro F, Auer T, Bellec P, Capotă M, et al. (2017) BIDS apps: Improving ease of use, accessibility, and reproducibility of neuroimaging data analysis methods. PLOS Computational Biology 13(3): e1005209. doi:10.1371/journal.pcbi.1005209.

5.Rahul S. Desikan, Florent Ségonne, Bruce Fischl, Brian T. Quinn, Bradford C. Dickerson, Deborah Blacker, Randy L. Buckner, Anders M. Dale, R. Paul Maguire, Bradley T. Hyman, Marilyn S. Albert, Ronald J. Killiany. An automated labeling system for subdividing the human cerebral cortex on MRI scans into gyral based regions of interest, NeuroImage. Volume 31, Issue 3, 2006, pp. 968-980,doi:10.1016/j.neuroimage.2006.01.021. 

6. 

> [3] 

> [4] 

> [5] 

> [6] 

> [7] 

> [8] 

> [9] 

> [10] 

> [11] 

### Usage
This App has the following command line arguments:

        $ docker -ti --rm sebastientourbier/multiscalebrainparcellator --help

        usage: multiscalebrainparcellator_bidsapp_entrypointscript [-h]
                                        [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
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
          --thalamic_nuclei     Segment thalamic thalamic_nuclei
          --hippocampal_subfields Segment hippocampal subfields (FreeSurfer)
          --brainstem_structures Segment brainstem structures (FreeSurfer)
          -v, --version         show program's version number and exit

#### Participant level
To run it in participant level mode (for one participant):

        docker run -it --rm \
        -v /home/localadmin/data/ds001:/bids_dataset \
        -v /media/localadmin/data/ds001/derivatives:/bids_dataset/derivatives \
        -v /usr/local/freesurfer/license.txt:/opt/freesurfer/license.txt \
        sebastientourbier/multiscalebrainparcellator:latest \
        /bids_dataset /bids_dataset/derivatives participant --participant_label 01 \
        --thalamic_nuclei \
        --hippocampal_subfields \
        --brainstem_structures

### Credits
* Patric Hagmann (pahagman)
* Sebastien Tourbier (sebastientourbier)
* Yasser Aleman (yasseraleman)
* Alessandra Griffa (agriffa)

### Funding
Work supported by the [Sinergia SNF-170873 Grant](http://p3.snf.ch/Project-170873).

### Copyright
Copyright (C) 2009-2019, Brain Communication Pathways Sinergia Consortium and the Multi Scale Brain Parcellator developers, Switzerland.
