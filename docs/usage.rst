=====
Usage
=====

To use Services-Communicator in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'services_communicator.apps.services_communicator',
        ...
    )

Add Services-Communicator's URL patterns:

.. code-block:: python

    from services_communicator import urls as services_communicator_urls


    urlpatterns = [
        ...
        url(r'^', include(services_communicator_urls)),
        ...
    ]
