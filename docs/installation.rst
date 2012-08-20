
============
Installation
============

This section contains information about how to download and install
django-email-change in your system. It also contains brief instructions about how
to build the included documentation.


Requirements
============

This application requires Python_ 2.4 or later and a functional installation
of Django_.

.. _Python: http://python.org
.. _Django: http://www.djangoproject.com

Detailed information about the minimum supported Django version and other
Python modules that may be required in order to run this software is shown
below:

.. literalinclude:: ../requirements.txt

This information exists in the ``requirements.txt`` file inside the
django-email-change distribution package. If ``pip`` is used to install this software,
then all these dependencies will also be installed, if they are not already
installed in your system.


Download
========

You can download the latest django-email-change releases from the `releases page`_ at
the *Python Package Index* (PyPI).

.. _`releases page`: http://pypi.python.org/pypi/django-email-change

Alternatively, you can clone the project's public source code repository
and then check-out any stable release, all of which are tagged::

    hg clone https://source.codetrax.org/hgroot/django-email-change
    hg tags
    hg update 0.1.0


Install
=======

To install django-email-change, use the provided installation script::

    python setup.py install

You can install ``django-email-change`` using ``pip``::

    pip install django-email-change

Or use ``easy_install``::

    easy_install -Z django-email-change

Note: the ``-Z`` flag is required to force ``easy_install`` to do a normal
source install rather than a zipped egg; django-email-change cannot be
used from a zipped egg install.

Alternatively, you can simply place the ``email_change`` directory,
which exists under the ``src`` directory, somewhere on your Python path
or symlink to it from somewhere on your Python path.

Finally, it is also possible to install this application directly from
the `source code repository`_ using ``pip``::

    pip install -e hg+https://source.codetrax.org/hgroot/django-email-change#egg=django-email-change

The above command will install the latest development release of
django-email-change.

To install a stable release directly from the `source code repository`_,
for instance, the ``0.1.0`` release, run the following command::

    pip install -e hg+https://source.codetrax.org/hgroot/django-email-change@0.1.0#egg=django-email-change-0.1.0

Please note that the mercurial_ source control management tool is required
for this operation.

.. _mercurial: http://mercurial.selenic.com/
.. _`source code repository`: https://source.codetrax.org/hgroot/django-email-change


How to build the documentation
==============================

This project's documentation is located in source form under the ``docs``
directory. In order to convert the documentation to a format that is
easy to read and navigate you need the ``sphinx`` package.

You can install ``sphinx`` using ``pip``::

    pip install sphinx

Or ``easy_install``::

    easy_install sphinx

Once ``sphinx`` is installed, change to the ``docs`` directory, open a shell
and run the following command::

    make html

This will build a HTML version of the documentation. You can read the
documentation by opening the following file in any web browser::

    docs/_build/html/index.html

