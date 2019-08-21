# Copyright (C) 2017-2019, Brain Communication Pathways Sinergia Consortium, Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

""" CMP segmentation stage
"""

# General imports
import os
from traits.api import *
import pickle
import gzip
import shutil
import pkg_resources
import multiprocessing as mp

# Nipype imports
import nipype.pipeline.engine as pe
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.fsl as fsl
import nipype.interfaces.ants as ants
from nipype.interfaces.io import FreeSurferSource
import nipype.interfaces.utility as util


# Own imports
from cmp.multiscalebrainparcellator.stages.common import Stage
#from cmp.interfaces.freesurfer import copyBrainMaskToFreesurfer, copyFileToFreesurfer

class SegmentationConfig(HasTraits):
    seg_tool = Enum(["Freesurfer"])
    make_isotropic = Bool(False)
    isotropic_vox_size = Float(1.2, desc='specify the size (mm)')
    isotropic_interpolation = Enum('cubic', 'weighted', 'nearest', 'sinc', 'interpolate',
                                desc='<interpolate|weighted|nearest|sinc|cubic> (default is cubic)')
    
    number_of_cores = 1
    # brain_mask_extraction_tool = Enum("Freesurfer",["Freesurfer","BET","ANTs","Custom"])
    # ants_templatefile = File(desc="Anatomical template")
    # ants_probmaskfile = File(desc="Brain probability mask")
    # ants_regmaskfile = File(desc="Mask (defined in the template space) used during registration for brain extraction.To limit the metric computation to a specific region.")

    # use_fsl_brain_mask = Bool(False)
    # brain_mask_path = File
    # use_existing_freesurfer_data = Bool(False)

    # freesurfer_subjects_dir = Directory
    # freesurfer_subject_id_trait = List
    # freesurfer_subject_id = Str
    # freesurfer_args = Str

    #white_matter_mask = File(exist=True)

    # def _freesurfer_subjects_dir_changed(self, old, new):
    #     dirnames = [name for name in os.listdir(self.freesurfer_subjects_dir) if
    #          os.path.isdir(os.path.join(self.freesurfer_subjects_dir, name))]
    #     self.freesurfer_subject_id_trait = dirnames

    # def _use_existing_freesurfer_data_changed(self,new):
    #     if new == True:
    #         self.custom_segmentation = False

def extract_base_directory(file):
    print "Extract reconall base dir : %s" % file[:-17]
    return file[:-17]


class SegmentationStage(Stage):
    # General and UI members
    def __init__(self):
        self.name = 'segmentation_stage'
        self.config = SegmentationConfig()
        self.inputs = ["T1","brain_mask"]
        self.outputs = ["subjects_dir","subject_id","custom_wm_mask","brain_mask","brain"]

    def create_workflow(self, flow, inputnode, outputnode):
        if self.config.seg_tool == "Freesurfer":
            # Converting to .mgz format
            fs_mriconvert = pe.Node(interface=fs.MRIConvert(out_type="mgz",out_file="T1.mgz"),name="mgz_convert")

            if self.config.make_isotropic:
                fs_mriconvert.inputs.vox_size = (self.config.isotropic_vox_size,self.config.isotropic_vox_size,self.config.isotropic_vox_size)
                fs_mriconvert.inputs.resample_type = self.config.isotropic_interpolation

            rename = pe.Node(util.Rename(), name="copy_orig")
            orig_dir = os.path.join(self.config.freesurfer_subject_id,"mri","orig")
            if not os.path.exists(orig_dir):
                os.makedirs(orig_dir)
                print "Folder not existing; %s created!" % orig_dir
            rename.inputs.format_string = os.path.join(orig_dir,"001.mgz")

            # ReconAll => named outputnode as we don't want to select a specific output....
            fs_reconall = pe.Node(interface=fs.ReconAll(flags='-no-isrunning -parallel -openmp {}'.format(self.config.number_of_cores)),name="reconall")
            fs_reconall.inputs.directive = 'all'
            #fs_reconall.inputs.args = self.config.freesurfer_args

            #fs_reconall.inputs.subjects_dir and fs_reconall.inputs.subject_id set in cmp/pipelines/diffusion/diffusion.py
            fs_reconall.inputs.subjects_dir = self.config.freesurfer_subjects_dir

            # fs_reconall.inputs.hippocampal_subfields_T1 = self.config.segment_hippocampal_subfields
            # fs_reconall.inputs.brainstem = self.config.segment_brainstem

            def isavailable(file):
                print "T1 is available"
                return file

            flow.connect([
                        (inputnode,fs_mriconvert,[(('T1',isavailable),'in_file')]),
                        (fs_mriconvert,rename,[('out_file','in_file')]),
                        (rename,fs_reconall,[(("out_file",extract_base_directory),"subject_id")]),
                        (fs_reconall,outputnode,[('subjects_dir','subjects_dir'),('subject_id','subject_id')]),
                        ])

    def has_run(self):
        return os.path.exists(os.path.join(self.stage_dir,"reconall","result_reconall.pklz"))
