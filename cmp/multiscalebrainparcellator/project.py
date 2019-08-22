# Copyright (C) 2017-2019, Brain Communication Pathways Sinergia Consortium, Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

""" Multi-scale Brain Parcellator Controler for handling non GUI general events
"""
import warnings
warnings.filterwarnings("ignore", message="No valid root directory found for domain 'derivatives'.")

# Global imports
import ast
from traits.api import *

import shutil
import os
import gzip
import glob
import string
import fnmatch
import multiprocessing
from subprocess import Popen

import ConfigParser

#PyBIDS import
from bids import BIDSLayout

# Own imports
from pipelines.anatomical import anatomical as Anatomical_pipeline
from cmtklib.bids.utils import write_derivative_description
from cmtklib.util import bcolors

class CMP_Project_Info(HasTraits):
    base_directory = Directory
    output_directory = Directory

    bids_layout = Instance(BIDSLayout)
    subjects = List([])
    subject = Enum(values='subjects')

    number_of_subjects = Int()

    subject_sessions = List([])
    subject_session = Enum(values='subject_sessions')

    #process_type = Enum('diffusion',['diffusion','fMRI'])
    parcellation_scheme = Str('Lausanne2008')
    atlas_info = Dict()
    freesurfer_subjects_dir = Str('')
    freesurfer_subject_id = Str('')

    t1_available = Bool(False)

    anat_config_error_msg = Str('')
    anat_config_to_load = Str()
    anat_available_config = List()
    anat_last_date_processed = Str('Not yet processed')
    anat_last_stage_processed = Str('Not yet processed')

    anat_stage_names = List
    anat_custom_last_stage = Str

    number_of_cores = Enum(1,range(1,multiprocessing.cpu_count()))


def fix_dataset_directory_in_pickles(local_dir, mode='local'):
    #mode can be local or bidsapp (local by default)

    searchdir = os.path.join(local_dir,'derivatives/cmp')

    for root, dirs, files in os.walk(searchdir):
        files = [ fi for fi in files if fi.endswith(".pklz") ]

        print('----------------------------------------------------')

        for fi in files:
            print("Processing file {} {} {}".format(root,dirs,fi))
            pick = gzip.open(os.path.join(root,fi))
            cont = pick.read()

            # Change pickles: bids app dataset directory -> local dataset directory
            if (mode == 'local') and cont.find('/bids_dataset/derivatives') and (local_dir != '/bids_dataset'):
                new_cont = string.replace(cont,'V/bids_dataset','V{}'.format(local_dir))
                pref = fi.split(".")[0]
                with gzip.open(os.path.join(root,'{}.pklz'.format(pref)), 'wb') as f:
                    f.write(new_cont)

            # Change pickles: local dataset directory -> bids app dataset directory
            elif (mode == 'bidsapp') and not cont.find('/bids_dataset/derivatives') and (local_dir != '/bids_dataset'):
                new_cont = string.replace(cont,'V{}'.format(local_dir),'V/bids_dataset')
                pref = fi.split(".")[0]
                with gzip.open(os.path.join(root,'{}.pklz'.format(pref)), 'wb') as f:
                    f.write(new_cont)
    return True


def remove_aborded_interface_pickles(local_dir):

    searchdir = os.path.join(local_dir,'derivatives/cmp')

    for root, dirs, files in os.walk(searchdir):
        files = [ fi for fi in files if fi.endswith(".pklz") ]

        print('----------------------------------------------------')

        for fi in files:
            print("Processing file {} {} {}".format(root,dirs,fi))
            try:
                cont = pickle.load(gzip.open(os.path.join(root,fi)))
            except Exception as e:
                # Remove pickle if unpickling error raised
                print('Unpickling Error: removed {}'.format(os.path.join(root,fi)))
                os.remove(os.path.join(root,fi))

def get_process_detail(project_info, section, detail):
    config = ConfigParser.ConfigParser()
    #print('Loading config from file: %s' % project_info.config_file)
    config.read(project_info.config_file)
    return config.get(section, detail)

def get_anat_process_detail(project_info, section, detail):
    config = ConfigParser.ConfigParser()
    #print('Loading config from file: %s' % project_info.config_file)
    config.read(project_info.anat_config_file)
    res = None
    if detail == "atlas_info":
        res = ast.literal_eval(config.get(section, detail))
    else:
        res = config.get(section, detail)
    return res

def anat_save_config(pipeline, config_path):
    config = ConfigParser.RawConfigParser()
    config.add_section('Global')
    global_keys = [prop for prop in pipeline.global_conf.traits().keys() if not 'trait' in prop] # possibly dangerous..?
    for key in global_keys:
        #if key != "subject" and key != "subjects":
        config.set('Global', key, getattr(pipeline.global_conf, key))
    for stage in pipeline.stages.values():
        config.add_section(stage.name)
        stage_keys = [prop for prop in stage.config.traits().keys() if not 'trait' in prop] # possibly dangerous..?
        for key in stage_keys:
            keyval = getattr(stage.config, key)
            if 'config' in key: # subconfig
                stage_sub_keys = [prop for prop in keyval.traits().keys() if not 'trait' in prop]
                for sub_key in stage_sub_keys:
                    config.set(stage.name, key+'.'+sub_key, getattr(keyval, sub_key))
            else:
                config.set(stage.name, key, keyval)

    config.add_section('Multi-processing')
    config.set('Multi-processing','number_of_cores',pipeline.number_of_cores)

    with open(config_path, 'wb') as configfile:
        config.write(configfile)

    print('  * Config file (anat) saved as {}'.format(config_path))

def anat_load_config(pipeline, config_path):
    config = ConfigParser.ConfigParser()
    config.read(config_path)
    global_keys = [prop for prop in pipeline.global_conf.traits().keys() if not 'trait' in prop] # possibly dangerous..?
    for key in global_keys:
        if key != "subject" and key != "subjects" and key != "subject_session" and key != "subject_sessions" and key != 'modalities':
            conf_value = config.get('Global', key)
            setattr(pipeline.global_conf, key, conf_value)
    for stage in pipeline.stages.values():
        stage_keys = [prop for prop in stage.config.traits().keys() if not 'trait' in prop] # possibly dangerous..?
        for key in stage_keys:
            if 'config' in key: #subconfig
                sub_config = getattr(stage.config, key)
                stage_sub_keys = [prop for prop in sub_config.traits().keys() if not 'trait' in prop]
                for sub_key in stage_sub_keys:
                    try:
                        conf_value = config.get(stage.name, key+'.'+sub_key)
                        try:
                            conf_value = eval(conf_value)
                        except:
                            pass
                        setattr(sub_config, sub_key, conf_value)
                    except:
                        pass
            else:
                try:
                    conf_value = config.get(stage.name, key)
                    try:
                        conf_value = eval(conf_value)
                    except:
                        pass
                    setattr(stage.config, key, conf_value)
                except:
                    pass
    setattr(pipeline,'number_of_cores',int(config.get('Multi-processing','number_of_cores')))

    return True

## Creates (if needed) the folder hierarchy
#
def refresh_folder(bids_directory,derivatives_directory, subject, input_folders, session=None):
    paths = []

    if session == None or session == '':
        paths.append(os.path.join(derivatives_directory,'freesurfer',subject))
        paths.append(os.path.join(derivatives_directory,'cmp',subject))

        for in_f in input_folders:
            paths.append(os.path.join(derivatives_directory,'cmp',subject,in_f))

        paths.append(os.path.join(derivatives_directory,'nipype',subject))
    else:
        paths.append(os.path.join(derivatives_directory,'freesurfer','%s_%s'%(subject,session)))
        paths.append(os.path.join(derivatives_directory,'cmp',subject,session))

        for in_f in input_folders:
            paths.append(os.path.join(derivatives_directory,'cmp',subject,session,in_f))

        paths.append(os.path.join(derivatives_directory,'nipype',subject,session))

    for full_p in paths:
        if not os.path.exists(full_p):
            try:
                os.makedirs(full_p)
            except os.error:
                print "%s was already existing" % full_p
            finally:
                print "Created directory %s" % full_p

    write_derivative_description(bids_directory, derivatives_directory, 'cmp')
    write_derivative_description(bids_directory, derivatives_directory, 'freesurfer')
    write_derivative_description(bids_directory, derivatives_directory, 'nipype')

def init_anat_project(project_info, is_new_project):
    anat_pipeline = Anatomical_pipeline.AnatomicalPipeline(project_info)

    bids_directory = os.path.abspath(project_info.base_directory)
    derivatives_directory = os.path.join(project_info.output_directory)

    if (project_info.subject_session != '') and (project_info.subject_session != None) :
        print('  * Prepare derivatives folder WITH session')
        refresh_folder(bids_directory, derivatives_directory, project_info.subject, anat_pipeline.input_folders, session=project_info.subject_session)
    else:
        print('  * Prepare derivatives folder WITHOUT session')
        refresh_folder(bids_directory, derivatives_directory, project_info.subject, anat_pipeline.input_folders)

    if is_new_project and anat_pipeline!= None: #and dmri_pipeline!= None:
        print('  * New project with newly created (or overwritten) configuration file')
        if not os.path.exists(derivatives_directory):
            try:
                os.makedirs(derivatives_directory)
            except os.error:
                print('    - {} was already existing'.format(derivatives_directory))
            finally:
                print('    - Created directory {}'.format(derivatives_directory))

        if (project_info.subject_session != '') and (project_info.subject_session != None) :
            project_info.anat_config_file = os.path.join(derivatives_directory,'%s_%s_anatomical_config.ini' % (project_info.subject,project_info.subject_session))
        else:
            project_info.anat_config_file = os.path.join(derivatives_directory,'%s_anatomical_config.ini' % (project_info.subject))
        #project_info.dmri_config_file = os.path.join(derivatives_directory,'%s_diffusion_config.ini' % (project_info.subject))

        if os.path.exists(project_info.anat_config_file):
            print(bcolors.WARNING + '  * Configuration file {} overwritten !'.format(project_info.anat_config_to_load)+bcolors.ENDC)
            anat_save_config(anat_pipeline, project_info.anat_config_file)
        else:
            anat_save_config(anat_pipeline, project_info.anat_config_file)

    else:
        print('  * Existing project... ')
        print('    - Loading configuration file {}'.format(project_info.anat_config_file))
        #print anat_pipeline.global_conf.subjects
        anat_conf_loaded = anat_load_config(anat_pipeline, project_info.anat_config_file)

        if not anat_conf_loaded:
            return None

    #print anat_pipeline
    anat_pipeline.config_file = project_info.anat_config_file

    return anat_pipeline

def update_anat_last_processed(project_info, pipeline):
    # last date
    if os.path.exists(os.path.join(project_info.base_directory,'derivatives','cmp',project_info.subject)):
        out_dirs = os.listdir(os.path.join(project_info.base_directory,'derivatives','cmp',project_info.subject))
        # for out in out_dirs:
        #     if (project_info.last_date_processed == "Not yet processed" or
        #         out > project_info.last_date_processed):
        #         pipeline.last_date_processed = out
        #         project_info.last_date_processed = out

        if (project_info.anat_last_date_processed == "Not yet processed" or
            pipeline.now > project_info.anat_last_date_processed):
            pipeline.anat_last_date_processed = pipeline.now
            project_info.anat_last_date_processed = pipeline.now

    # last stage
    if os.path.exists(os.path.join(project_info.base_directory,'derivatives','cmp',project_info.subject,'tmp','anatomical_pipeline')):
        stage_dirs = []
        for root, dirnames, _ in os.walk(os.path.join(project_info.base_directory,'derivatives','cmp',project_info.subject,'tmp','anatomical_pipeline')):
            for dirname in fnmatch.filter(dirnames, '*_stage'):
                stage_dirs.append(dirname)
        for stage in pipeline.ordered_stage_list:
            if stage.lower()+'_stage' in stage_dirs:
                pipeline.last_stage_processed = stage
                project_info.anat_last_stage_processed = stage

    # last parcellation scheme
    project_info.parcellation_scheme = pipeline.parcellation_scheme
    project_info.atlas_info = pipeline.atlas_info

def create_configuration_file_participant_level(bids_dir,output_dir,subjects,subject,subject_session,resolution,thalamic_nuclei,hippocampal_subfields,brainstem_structures,multiproc_number_of_cores=1,fs_number_of_cores=1):

    project_info = CMP_Project_Info()
    project_info.base_directory = bids_dir
    project_info.output_directory = output_dir
    project_info.subjects = subjects
    project_info.subject = subject
    project_info.number_of_cores = multiproc_number_of_cores

    if subject_session != '':
        project_info.subject_sessions = ['{}'.format(subject_session)]
        project_info.subject_session = subject_session
    else:
        project_info.subject_sessions = ['']
        project_info.subject_session = ''

    anat_pipeline = init_anat_project(project_info, True)

    anat_pipeline.stages['Segmentation'].config.make_isotropic = True
    anat_pipeline.stages['Segmentation'].config.isotropic_vox_size = resolution
    anat_pipeline.stages['Segmentation'].config.isotropic_interpolation = 'interpolate'
    anat_pipeline.stages['Segmentation'].config.fs_number_of_cores = fs_number_of_cores

    anat_pipeline.stages['Parcellation'].config.include_thalamic_nuclei_parcellation = thalamic_nuclei
    anat_pipeline.stages['Parcellation'].config.segment_hippocampal_subfields = hippocampal_subfields
    anat_pipeline.stages['Parcellation'].config.segment_brainstem = brainstem_structures
    anat_pipeline.stages['Parcellation'].config.fs_number_of_cores = fs_number_of_cores

    anat_save_config(pipeline=anat_pipeline,config_path=anat_pipeline.config_file)
    return project_info, anat_pipeline.config_file

def run(command, env={}):
    import subprocess
    merged_env = os.environ
    merged_env.update(env)
    process = subprocess.Popen(command, shell=True,
                               env=merged_env)

    # if process.returncode != 0:
    #     raise Exception("Non zero return code: %d"%process.returncode)

    return process

def participant_level_process(project_info, configuration_file):

    cmd = ['multiscalebrainparcellator',
                                        '{}'.format(project_info.base_directory),
                                        '{}'.format(project_info.output_directory),
                                        '{}'.format(project_info.subject)]

    if project_info.subject_session != '':
        cmd.append('{}'.format(project_info.subject_session))

    cmd.append('{}'.format(configuration_file))
    cmd = ' '.join(cmd)

    print(' * Command: {}'.format(cmd))

    # if project_info.subject_session != '':
    #     log_filename = os.path.join(project_info.output_directory,'cmp','{}_{}log-cmpbidsapp.txt'.format(participant_label))
    # else:
    #     log_filename = os.path.join(project_info.output_directory,'cmp','sub-{}_log-cmpbidsapp.txt'.format(participant_label))

    if not os.path.exists(os.path.join(project_info.output_directory,'cmp')):
        os.makedirs(os.path.join(project_info.output_directory,'cmp'))

    # with open(log_filename, 'w+') as log:
    #     proc = Popen(cmd, stdout=log, stderr=log)
    #     #docker_process.communicate()

    #import subprocess
    #proc = subprocess.call(cmd)

    proc = run(cmd)
    return proc


def manage_procs(proclist):
    for proc in proclist:
        if proc.poll() is not None:
            proclist.remove(proc)
