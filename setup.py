#!/usr/bin/env python

"""Multi-scale Brain Parcellator and CMTKlib
"""
import os
import sys
from glob import glob
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

packages=["cmp",
          "cmp.interfaces",
          "cmp.multiscalebrainparcellator",
          "cmp.multiscalebrainparcellator.stages",
          "cmp.multiscalebrainparcellator.stages.segmentation",
          "cmp.multiscalebrainparcellator.stages.parcellation",
          "cmp.multiscalebrainparcellator.pipelines",
          "cmp.multiscalebrainparcellator.pipelines.anatomical",
          "cmtklib",
          "cmtklib.bids"]

package_data = {'cmtklib':
                ['data/parcellation/lausanne2008/*/*.*',
                 'data/parcellation/lausanne2018/*.*',
                 'data/parcellation/lausanne2018/*/*.*',
                'data/parcellation/nativefreesurfer/*/*.*',
                'data/colortable_and_gcs/*.*',
                'data/colortable_and_gcs/my_atlas_gcs/*.*',
                'data/segmentation/thalamus2018/*.*']
                }

################################################################################
# For some commands, use setuptools

if len(set(('develop', 'bdist_egg', 'bdist_rpm', 'bdist', 'bdist_dumb',
            'bdist_wininst', 'install_egg_info', 'egg_info', 'easy_install',
            )).intersection(sys.argv)) > 0:
    from setup_egg import extra_setuptools_args

# extra_setuptools_args can be defined from the line above, but it can
# also be defined here because setup.py has been exec'ed from
# setup_egg.py.
if not 'extra_setuptools_args' in globals():
    extra_setuptools_args = dict()

def main(**extra_args):
    from distutils.core import setup
    from cmp.multiscalebrainparcellator.info import __version__
    setup(name='multiscalebrainparcellator',
          version=__version__,
          description='Multi-scale Brain Parcellator',
          long_description="""The Multi-scale Brain Parcellator implements a full processing pipeline, from raw T1 to multi-scale brain parcellations. """ + \
          """The Multi-scale Brain Parcellator is part of upcoming new release of the Connectome Mapper 3, part of the Connectome Mapping Toolkit.""",
          author= 'Sebastien Tourbier',
          author_email='sebastien.tourbier@alumni.epfl.ch',
          url='http://www.connectomics.org/',
          scripts = ['scripts/multiscalebrainparcellator','scripts/multiscalebrainparcellator_bidsapp_entrypointscript'],
          license='Modified BSD License',
          packages = packages,
        classifiers = [c.strip() for c in """\
            Development Status :: 1 - Beta
            Intended Audience :: Developers
            Intended Audience :: Science/Research
            Operating System :: OS Independent
            Programming Language :: Python
            Topic :: Scientific/Engineering
            Topic :: Software Development
            """.splitlines() if len(c.split()) > 0],
          maintainer = 'Brain Communication Pathways Sinergia Consortium',
          maintainer_email = 'sebastien.tourbier@alumni.epfl.ch',
          package_data = package_data,
          requires=["numpy (>=1.2)", "nibabel (>=2.0.0)", "pybids (>=0.6.4)"],
          **extra_args
         )

if __name__ == "__main__":
    main(**extra_setuptools_args)
