=============================
Services-Communicator
=============================

.. image:: https://badge.fury.io/py/services_communicator.svg
    :target: https://badge.fury.io/py/services_communicator

.. image:: https://travis-ci.org/eshafik/services_communicator.svg?branch=master
    :target: https://travis-ci.org/eshafik/services_communicator

.. image:: https://codecov.io/gh/eshafik/services_communicator/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/eshafik/services_communicator

Communicator for internal services

Documentation
-------------

The full documentation is at https://services_communicator.readthedocs.io.

Quickstart
----------

Install Services-Communicator::

    pip install services_communicator

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'services_communicator.apps.services_communicator',
        ...
    )


Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox
