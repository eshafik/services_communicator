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

Make migrate to database::

    python manage.py migrate


Add CREDENTIALS on settings.py file::

    CREDENTIALS = { <service id>: {"username": <username>, "password": <password>},
                    <service id>: {"username": <username>, "password": <password>},
                    ..........................................................
                    }
    or,
    CREDENTIALS = { "<service slug>": {"username": <username>, "password": <password>},
                    "<service slug>": {"username": <username>, "password": <password>},
                    ..........................................................
                    }
    or,
    CREDENTIALS = { "<service guid>": {"username": <username>, "password": <password>},
                    "<service guid>": {"username": <username>, "password": <password>},
                    ..........................................................
                    }



Now make your own Communicator:

.. code-block:: python


    from services_communicator.communicator import Communicator

    class CustomCommunicator(Communicator):
        """ Create your custom method here like this by inheriting Communicator"""

        def get_roles(self, *args, **kwargs):
            """
                - To get other service roles
            :return:
            """
            path = self.service.get_full_url + "/users/get_role/" # service url extension to do this task
            response = self._get_action(path=path, headers=self._token())
            return response.json()

        def post_roles(self, *args, **kwargs):
            """
                - To create other service roles
            :return:
            """
            data = data
            path = self.service.get_full_url + "/users/create_role/" # service url extension to do this task
            response = self._post_action(path=path, data=data, headers=self._token())
            return response.json()

        def patch_roles(self, *args, **kwargs):
            """
                - To create other service roles
            :return:
            """
            data = data
            path = self.service.get_full_url + "/users/update_role/" # service url extension to do this task
            response = self._patch_action(path=path, data=data, headers=self._token())
            return response.json()


To perform action, initialize your CustomCommunicator and call your required methods:

.. code-block:: python

    service_communicator = CustomCommunicator(**{"service_id": <id>})
    or,
    service_communicator = CustomCommunicator(**{"service_slug": "<service slug>"})
    or,
    service_communicator = CustomCommunicator(**{"service_guid": "<service guid>"})

    Now you can call your methods to perform specific task:

    response = service_communicator.get_roles()



Precaution
----------

* This module is designed only for the personal development purpose.

