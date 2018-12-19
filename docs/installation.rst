************************
Installation Instruction
************************

.. warning:: This software is for research purposes only and shall not be used for
             any clinical use. This software has not been reviewed or approved by
             the Food and Drug Administration or equivalent authority, and is for
             non-clinical, IRB-approved Research Use Only. In no event shall data
             or images generated through the use of the Software be used in the
             provision of patient care.


The Multi-Scale Brain Parcellator is a BIDS App that relies on Docker. Make sure that you have Docker installed. Installation instructions are found in :ref:`manual-install-multiscalebrainparcellator`.

The Multi-Scale Brain Parcellator
===============================

Prerequisites
-------------

* Installed Docker Engine corresponding to your system:

  * For Ubuntu 14.04/16.04/18.04, follow the instructions from the web page::

    $ firefox https://docs.docker.com/install/linux/docker-ce/ubuntu/

  * For Mac OSX (>=10.10.3), get the .dmg installer from the web page::

    $ firefox https://store.docker.com/editions/community/docker-ce-desktop-mac

  * For Windows (>=10), get the installer from the web page::

    $ firefox https://store.docker.com/editions/community/docker-ce-desktop-windows

.. note:: Multi-Scale Brain Parcellator BIDSApp has been tested only on Ubuntu and MacOSX. For Windows users, it might be required to make few patches in the Dockerfile.


* For Ubuntu, Docker could be managed as a non-root user

  * Open a terminal

  * Create the docker group::

    $ sudo groupadd docker

  * Add the current user to the docker group::

    $ sudo usermod -G docker -a $USER

  * Reboot

    After reboot, test if docker is managed as non-root::

      $ docker run hello-world


.. _manual-install-multiscalebrainparcellator:

Manual installation
---------------------------------------

Installation and use of the Multi-Scale Brain Parcellator has been facilitated through the distribution of a Docker container image.

* Open a terminal

* Get the latest release of the BIDS App::

  $ docker pull sebastientourbier/multiscalebrainparcellator:latest

* To display all docker images available::

  $ docker images

You should see the docker image "multiscalebrainparcellator" with tag "latest" is now available.


Help/Questions
--------------

If you run into any problems or have any questions, you can post to the `CMTK-users group <http://groups.google.com/group/cmtk-users>`_. Code bugs can be reported by creating a "New Issue" on the `source code repository <https://github.com/sebastientourbier/multiscalebrainparcellator/issues>`_.
