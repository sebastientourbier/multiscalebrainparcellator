# Copyright (C) 2017-2019, Brain Communication Pathways Sinergia Consortium, Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

""" Common functions for CMP pipelines
"""

# General imports
import os
import fnmatch
import shutil
import threading
import multiprocessing
import time
from traits.api import *
#import apptools.io.api as io

# Nipype utils imports
from nipype.utils.filemanip import copyfile
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
from nipype.caching import Memory
from nipype.interfaces.base import CommandLineInputSpec, CommandLine, traits, BaseInterface, \
    BaseInterfaceInputSpec, File, TraitedSpec, isdefined, Directory, InputMultiPath
from nipype.utils.filemanip import split_filename

# Nipype interfaces
#from nipype.interfaces.dcm2nii import Dcm2niix
#import nipype.interfaces.diffusion_toolkit as dtk
#import nipype.interfaces.mrtrix as mrt
import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs

# Own import
import cmp.interfaces.fsl as cmp_fsl

class ProcessThread(threading.Thread):
    pipeline = Instance(Any)

    def run(self):
        self.pipeline.process()

class Pipeline(HasTraits):
    # informations common to project_info
    base_directory = Directory
    output_directory = Directory
    root = Property
    subject = Str
    subject_session = Str
    last_date_processed = Str
    last_stage_processed = Str

    # num core settings
    number_of_cores = 1

    #-- Traits Default Value Methods -----------------------------------------

    # def _base_directory_default(self):
    #     return getcwd()

    #-- Property Implementations ---------------------------------------------

    @property_depends_on('base_directory')
    def _get_root(self):
        return File(path=self.base_directory)

    @property_depends_on('output_directory')
    def _get_output(self):
        return File(path=self.output_directory)

    def __init__(self, project_info):
        self.base_directory = project_info.base_directory
        self.output_directory = project_info.output_directory
        self.subject = project_info.subject
        self.subject_session = project_info.subject_session
        self.number_of_cores = project_info.number_of_cores

        for stage in self.stages.keys():
            if project_info.subject_session != '':
                self.stages[stage].stage_dir = os.path.join(self.output_directory,'cmp',self.subject,project_info.subject_session,'tmp',self.pipeline_name,self.stages[stage].name)
            else:
                self.stages[stage].stage_dir = os.path.join(self.output_directory,'cmp',self.subject,'tmp',self.pipeline_name,self.stages[stage].name)

    def check_config(self):
        # if self.stages['Segmentation'].config.seg_tool ==  'Custom segmentation':
        #     if not os.path.exists(self.stages['Segmentation'].config.white_matter_mask):
        #         return('\nCustom segmentation selected but no WM mask provided.\nPlease provide an existing WM mask file in the Segmentation configuration window.\n')
        #     if not os.path.exists(self.stages['Parcellation'].config.atlas_nifti_file):
        #         return('\n\tCustom segmentation selected but no atlas provided.\nPlease specify an existing atlas file in the Parcellation configuration window.\t\n')
        #     if not os.path.exists(self.stages['Parcellation'].config.graphml_file):
        #         return('\n\tCustom segmentation selected but no graphml info provided.\nPlease specify an existing graphml file in the Parcellation configuration window.\t\n')
        # if self.stages['Connectome'].config.output_types == []:
        #     return('\n\tNo output type selected for the connectivity matrices.\t\n\tPlease select at least one output type in the connectome configuration window.\t\n')
        return ''

    def create_stage_flow(self, stage_name):
        stage = self.stages[stage_name]
        flow = pe.Workflow(name=stage.name)
        inputnode = pe.Node(interface=util.IdentityInterface(fields=stage.inputs),name="inputnode")
        outputnode = pe.Node(interface=util.IdentityInterface(fields=stage.outputs),name="outputnode")
        flow.add_nodes([inputnode,outputnode])
        stage.create_workflow(flow,inputnode,outputnode)
        return flow

    def launch_process(self):
        pt = ProcessThread()
        pt.pipeline = self
        pt.start()
