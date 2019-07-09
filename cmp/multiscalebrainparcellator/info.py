""" This file contains multiscalebrainparcellator package version information """

_version_major = 1
_version_minor = 0
_version_micro = 1
_version_extra = '-issue1' 

__release_date__ = '2019.01.10'

__minor_version__ = "%s.%s" % (_version_major,
                               _version_minor)

__version__ = "%s.%s.%s%s" % (_version_major,
                              _version_minor,
                              _version_micro,
                              _version_extra)

#__current_year__ = datetime.datetime.now().strftime("%Y")
__current_year__ = '2019'

__author__ = 'The Multi-Scale Brain Parcellator developers'
__copyright__ = 'Copyright {}, Brain Communication Pathways Sinergia Consortium'.format(__current_year__)
__credits__ = ('Contributors: please check the ``.zenodo.json`` file at the top-level folder'
               'of the repository')
__license__ = '3-clause BSD'
__maintainer__ = 'Sebastien Tourbier'
__email__ = 'sebastien.tourbier@alumni.epfl.ch'
__status__ = 'Prototype'

__packagename__ = 'multiscalebrainparcellator'

__url__ = 'https://github.com/sebastientourbier/{name}'.format(name=__packagename__)

DOWNLOAD_URL = (
    'https://github.com/sebastientourbier/{name}/archive/{ver}.tar.gz'.format(
        name=__packagename__, ver=__version__))
