lernito-openedx
###############

|pypi-badge| |ci-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge| |status-badge|

Purpose
*******

Lernito OpenedX is a Django application that provides webhook integration between Open edX and Lernito services.
It enables seamless communication and data synchronization between your Open edX instance and Lernito platform.

Getting Started with Development
********************************

Please see the Open edX documentation for `guidance on Python development`_ in this repo.

.. _guidance on Python development: https://docs.openedx.org/en/latest/developers/how-tos/get-ready-for-python-dev.html

Installation
************

To install this component in your Open edX instance:

1. Add the package to the requirements:

   .. code-block:: bash

       tutor config save --append OPENEDX_EXTRA_PIP_REQUIREMENTS=git+https://github.com/edSPIRIT/lernito-openedx.git

2. Save the secret in Tutor config:

   .. code-block:: bash

       tutor config save -s LERNITO_WEBHOOK_SECRET=YOUR_SECRET

3. You need to configure ``LERNITO_WEBHOOK_SECRET`` in your Django settings. This can be done in two ways:

   - For Tutor-managed installations:
     Create a Tutor plugin that adds the required setting:

     .. code-block:: python

         from tutor import hooks

         hooks.Filters.ENV_PATCHES.add_item(
             (
                 "openedx-common-settings",
                 "LERNITO_WEBHOOK_SECRET = '{{ LERNITO_WEBHOOK_SECRET }}'",
             )
         )

   - For non-Tutor installations:
     Add the setting directly to your Django settings file.

4. build the image and run the container:

   .. code-block:: bash

       tutor images build openedx  # or openedx-dev for local development
       tutor dev|local|k8s start

Webhook API Documentation
***********************

The webhook endpoint accepts POST requests for enrolling users in courses. It handles both existing and new users.

Endpoint
========

``POST /api/lernito/webhook/``

Request Headers
==============

- ``X-Lernito-Signature``: HMAC SHA256 signature of the request payload
- ``Content-Type: application/json``

Request Body
===========

.. code-block:: json

    {
        "email": "user@example.com",
        "name": "First",
        "family": "Last",
        "username": "username",
        "courseIds": ["course-v1:edX+DemoX+Demo_Course"]
    }

Response Scenarios
================

1. Successful Enrollment (200 OK)
--------------------------------

For existing users:

.. code-block:: json

    {
        "success": true,
        "message": "User enrollment status verified for 2 course(s)"
    }

For new users:

.. code-block:: json

    {
        "success": true,
        "message": "Enrollment allowance verified for 2 course(s)"
    }

2. Authentication Errors (401 UNAUTHORIZED)
----------------------------------------

Invalid signature:

.. code-block:: json

    {
        "success": false,
        "message": "Invalid signature"
    }

3. Validation Errors (400 BAD REQUEST)
------------------------------------

Invalid course:

.. code-block:: json

    {
        "success": false,
        "message": "Course course-v1:edX+DemoX+Demo_Course does not exist"
    }

Invalid course format:

.. code-block:: json

    {
        "success": false,
        "message": "Invalid course key format: invalid-course-id"
    }

Missing required fields:

.. code-block:: json

    {
        "success": false,
        "message": {
            "email": ["This field is required"],
            "courseIds": ["This field is required"]
        }
    }

4. Server Errors (500 INTERNAL SERVER ERROR)
-----------------------------------------

.. code-block:: json

    {
        "success": false,
        "message": "Internal server error"
    }

Behavior
========

The API is idempotent, meaning:

- For existing users: It will enroll them in courses if not already enrolled
- For new users: It will create enrollment permissions that activate upon registration
- Multiple identical requests will produce the same result without creating duplicates
- Each request verifies and ensures the enrollment status is correct

Testing
=======

You can test the webhook using the following Python script to generate a valid signature:

.. code-block:: python

    import hmac
    import hashlib
    import json

    # Your webhook data
    data = {
        "email": "test@example.com",
        "name": "Test",
        "family": "User",
        "username": "testuser",
        "courseIds": ["course-v1:edX+DemoX+Demo_Course"]
    }

    # Convert to sorted JSON string
    data_string = json.dumps(data, sort_keys=True)

    # Generate signature
    webhook_secret = "your_webhook_secret"
    signature = hmac.new(
        webhook_secret.encode('utf-8'),
        data_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    print(f"X-Lernito-Signature: {signature}")

Getting Help
************

Documentation
=============

PLACEHOLDER: Start by going through `the documentation`_.  If you need more help see below.

.. _the documentation: https://docs.openedx.org/projects/lernito-openedx

(TODO: `Set up documentation <https://openedx.atlassian.net/wiki/spaces/DOC/pages/21627535/Publish+Documentation+on+Read+the+Docs>`_)

More Help
=========

If you're having trouble, we have discussion forums at
https://discuss.openedx.org where you can connect with others in the
community.

Our real-time conversations are on Slack. You can request a `Slack
invitation`_, then join our `community Slack workspace`_.

For anything non-trivial, the best path is to open an issue in this
repository with as many details about the issue you are facing as you
can provide.

https://github.com/edSPIRIT/lernito-openedx/issues

For more information about these options, see the `Getting Help <https://openedx.org/getting-help>`__ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/

License
*******

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

Contributing
************

Contributions are very welcome.
Please read `How To Contribute <https://openedx.org/r/how-to-contribute>`_ for details.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to discuss your new feature idea with the maintainers before beginning development
to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

The Open edX Code of Conduct
****************************

All community members are expected to follow the `Open edX Code of Conduct`_.

.. _Open edX Code of Conduct: https://openedx.org/code-of-conduct/

People
******

The assigned maintainers for this component and other project details may be
found in `Backstage`_. Backstage pulls this data from the ``catalog-info.yaml``
file in this repo.

.. _Backstage: https://backstage.openedx.org/catalog/default/component/lernito-openedx

Reporting Security Issues
*************************

Please do not report security issues in public. Please email security@openedx.org.

.. |pypi-badge| image:: https://img.shields.io/pypi/v/lernito-openedx.svg
    :target: https://pypi.python.org/pypi/lernito-openedx/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/edSPIRIT/lernito-openedx/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/edSPIRIT/lernito-openedx/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/edSPIRIT/lernito-openedx/coverage.svg?branch=main
    :target: https://codecov.io/github/edSPIRIT/lernito-openedx?branch=main
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/lernito-openedx/badge/?version=latest
    :target: https://docs.openedx.org/projects/lernito-openedx
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/lernito-openedx.svg
    :target: https://pypi.python.org/pypi/lernito-openedx/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/edSPIRIT/lernito-openedx.svg
    :target: https://github.com/edSPIRIT/lernito-openedx/blob/main/LICENSE.txt
    :alt: License

.. TODO: Choose one of the statuses below and remove the other status-badge lines.
.. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red
