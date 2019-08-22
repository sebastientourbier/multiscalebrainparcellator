# Copyright (C) 2017-2019, Brain Communication Pathways Sinergia Consortium, Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

""" CMP Stage for Parcellation
"""

# General imports
from traits.api import *
import pkg_resources
import os
import pickle
import gzip
from traits.trait_handlers import TraitListObject

# Nipype imports
import nipype.pipeline.engine as pe          # pypeline engine
# import nipype.interfaces.cmtk as cmtk
import cmtklib as cmtk
import nipype.interfaces.utility as util

from cmtklib.parcellation import Parcellate, ParcellateBrainstemStructures, ParcellateHippocampalSubfields, ParcellateThalamus, CombineParcellations, ComputeParcellationRoiVolumes
# Own imports
from cmp.multiscalebrainparcellator.stages.common import Stage

class ParcellationConfig(HasTraits):
    parcellation_scheme = Str('Lausanne2018')
    parcellation_scheme_editor = List(['Lausanne2018'])
    include_thalamic_nuclei_parcellation = Bool(True)
    template_thalamus = File()
    thalamic_nuclei_maps = File()
    segment_hippocampal_subfields = Bool(True)
    segment_brainstem = Bool(True)
    pre_custom = Str('Lausanne2018')
    fs_number_of_cores = Int(1)
    #atlas_name = Str()
    #number_of_regions = Int()
    #atlas_nifti_file = File(exists=True)
    #csf_file = File(exists=True)
    #brain_file = File(exists=True)
    #graphml_file = File(exists=True)
    #atlas_info = Dict()

    # def update_atlas_info(self):
    #     atlas_name = os.path.basename(self.atlas_nifti_file)
    #     atlas_name = os.path.splitext(os.path.splitext(atlas_name)[0])[0].encode('ascii')
    #     self.atlas_info = {atlas_name : {'number_of_regions':self.number_of_regions,'node_information_graphml':self.graphml_file}}
    #     print "Update atlas information"
    #     print self.atlas_info
    #
    # def _atlas_nifti_file_changed(self,new):
    #     self.update_atlas_info()
    #
    # def _number_of_regions_changed(self,new):
    #     self.update_atlas_info()
    #
    # def _graphml_file_changed(self,new):
    #     self.update_atlas_info()
    #
    # def _parcellation_scheme_changed(self,old,new):
    #     if new == 'Custom':
    #         self.pre_custom = old

class ParcellationStage(Stage):

    def __init__(self):
        self.name = 'parcellation_stage'
        self.config = ParcellationConfig()
        self.config.template_thalamus = pkg_resources.resource_filename('cmtklib', os.path.join('data', 'segmentation', 'thalamus2018', 'mni_icbm152_t1_tal_nlin_sym_09b_hires_1.nii.gz'))
        self.config.thalamic_nuclei_maps = pkg_resources.resource_filename('cmtklib', os.path.join('data', 'segmentation', 'thalamus2018', 'Thalamus_Nuclei-HCP-4DSPAMs.nii.gz'))
        self.inputs = ["subjects_dir","subject_id","custom_wm_mask"]
        self.outputs = [#"aseg_file",
            "T1","brain","aseg","brain_mask",
    		"wm_mask_file",
            "wm_eroded",
            "csf_eroded",
            "brain_eroded",
            "gm_mask_file",
            "aseg","aparc_aseg",
    	       #"cc_unknown_file","ribbon_file","roi_files",
            "roi_volumes","roi_colorLUTs","roi_graphMLs","roi_volumes_stats",
            "parcellation_scheme","atlas_info"]

    def create_workflow(self, flow, inputnode, outputnode):
        outputnode.inputs.parcellation_scheme = self.config.parcellation_scheme

        if self.config.parcellation_scheme != "Custom":

            parc_node = pe.Node(interface=Parcellate(),name="%s_parcellation" % self.config.parcellation_scheme)
            parc_node.inputs.parcellation_scheme = self.config.parcellation_scheme
            parc_node.inputs.erode_masks = True

            flow.connect([
                         (inputnode,parc_node,[("subjects_dir","subjects_dir"),(("subject_id",os.path.basename),"subject_id")]),
                         (parc_node,outputnode,[#("aseg_file","aseg_file"),("cc_unknown_file","cc_unknown_file"),
                                                #("ribbon_file","ribbon_file"),("roi_files","roi_files"),
    					     ("white_matter_mask_file","wm_mask_file"),
                             ("gray_matter_mask_file","gm_mask_file"),
                             #("roi_files_in_structural_space","roi_volumes"),
                             ("wm_eroded","wm_eroded"),("csf_eroded","csf_eroded"),("brain_eroded","brain_eroded"),
                             ("T1","T1"),("brain","brain"),("brain_mask","brain_mask")])
                        ])

            flow.connect([
                        (parc_node,outputnode,[("aseg","aseg")]),
                        ])

            if self.config.parcellation_scheme == 'Lausanne2018':
                parcCombiner = pe.Node(interface=CombineParcellations(),name="parcCombiner")
                parcCombiner.inputs.create_colorLUT = True
                parcCombiner.inputs.create_graphml = True

                flow.connect([
                            (inputnode,parcCombiner,[("subjects_dir","subjects_dir"),(("subject_id",os.path.basename),"subject_id")]),
                            (parc_node,parcCombiner,[("roi_files_in_structural_space","input_rois")]),
                            ])

                if self.config.segment_brainstem:
                    parcBrainStem = pe.Node(interface=ParcellateBrainstemStructures(number_of_cores=self.config.fs_number_of_cores),name="parcBrainStem")

                    flow.connect([
                                (inputnode,parcBrainStem,[("subjects_dir","subjects_dir"),(("subject_id",os.path.basename),"subject_id")]),
                                (parcBrainStem,parcCombiner,[("brainstem_structures","brainstem_structures")]),
                                ])

                if self.config.segment_hippocampal_subfields:
                    parcHippo = pe.Node(interface=ParcellateHippocampalSubfields(number_of_cores=self.config.fs_number_of_cores),name="parcHippo")

                    flow.connect([
                                (inputnode,parcHippo,[("subjects_dir","subjects_dir"),(("subject_id",os.path.basename),"subject_id")]),
                                (parcHippo,parcCombiner,[("lh_hipposubfields","lh_hippocampal_subfields")]),
                                (parcHippo,parcCombiner,[("rh_hipposubfields","rh_hippocampal_subfields")]),
                                ])

                if self.config.include_thalamic_nuclei_parcellation:
                    parcThal = pe.Node(interface=ParcellateThalamus(),name="parcThal")
                    parcThal.inputs.template_image = self.config.template_thalamus
                    parcThal.inputs.thalamic_nuclei_maps = self.config.thalamic_nuclei_maps

                    flow.connect([
                                (inputnode,parcThal,[("subjects_dir","subjects_dir"),(("subject_id",os.path.basename),"subject_id")]),
                                (parc_node,parcThal,[("T1","T1w_image")]),
                                (parcThal,parcCombiner,[("max_prob_registered","thalamus_nuclei")]),
                                ])

                flow.connect([
                            (parcCombiner,outputnode,[("aparc_aseg","aparc_aseg")]),
                            (parcCombiner,outputnode,[("output_rois","roi_volumes")]),
                            (parcCombiner,outputnode,[("colorLUT_files","roi_colorLUTs")]),
                            (parcCombiner,outputnode,[("graphML_files","roi_graphMLs")]),
                        ])

                computeROIVolumetry = pe.Node(interface=ComputeParcellationRoiVolumes(), name='computeROIVolumetry')
                computeROIVolumetry.inputs.parcellation_scheme = self.config.parcellation_scheme
                
                flow.connect([
                            (parcCombiner,computeROIVolumetry,[("output_rois","roi_volumes")]),
                            (parcCombiner,computeROIVolumetry,[("graphML_files","roi_graphMLs")]),
                            (computeROIVolumetry,outputnode, [("roi_volumes_stats","roi_volumes_stats")]),
                            ])


                    # create_atlas_info = pe.Node(interface=CreateLausanne2018AtlasInfo(),name="create_atlas_info")
                    # flow.connect([
                    #             (parcCombiner,create_atlas_info,[("output_rois","roi_volumes")]),
                    #             (parcCombiner,create_atlas_info,[("graphML_files","roi_graphMLs")]),
                    #             (create_atlas_info,outputnode,[("atlas_info","atlas_info")]),
                    #         ])
            else:
                flow.connect([
                            (parc_node,outputnode,[("aparc_aseg","aparc_aseg")]),
                            (parc_node,outputnode,[("roi_files_in_structural_space","roi_volumes")]),
                        ])

        else:
            temp_node = pe.Node(interface=util.IdentityInterface(fields=["roi_volumes","atlas_info"]),name="custom_parcellation")
            temp_node.inputs.roi_volumes = self.config.atlas_nifti_file
            temp_node.inputs.atlas_info = self.config.atlas_info
            flow.connect([
                        (temp_node,outputnode,[("roi_volumes","roi_volumes")]),
                        (temp_node,outputnode,[("atlas_info","atlas_info")]),
                        (inputnode,outputnode,[("custom_wm_mask","wm_mask_file")])
                        ])
            import cmp.interfaces.fsl as fsl
            threshold_roi = pe.Node(interface=fsl.BinaryThreshold(thresh=0.0,binarize=True,out_file='T1w_class-GM.nii.gz'),name='threshold_roi_bin')

            def get_first(roi_volumes):
                return roi_volumes

            flow.connect([
                        (temp_node,threshold_roi,[(("roi_volumes",get_first),"in_file")]),
                        (threshold_roi,outputnode,[("out_file","gm_mask_file")]),
                        ])

    def has_run(self):
        if self.config.parcellation_scheme != "Custom":
            if self.config.parcellation_scheme == 'Lausanne2018':
                return os.path.exists(os.path.join(self.stage_dir,"parcCombiner","result_parcCombiner.pklz"))
            else:
                return os.path.exists(os.path.join(self.stage_dir,"%s_parcellation" % self.config.parcellation_scheme,"result_%s_parcellation.pklz" % self.config.parcellation_scheme))
        else:
            return os.path.exists(self.config.atlas_nifti_file)
