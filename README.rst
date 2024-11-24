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

Deploying
*********

To deploy this component in your Open edX instance:

1. Install the package using pip:

   .. code-block:: bash

       pip install lernito-openedx

2. Add required configuration:

   You need to configure ``LERNITO_WEBHOOK_SECRET`` in your Django settings. This can be done in two ways:

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

3. Add the application to your INSTALLED_APPS:

   .. code-block:: python

       INSTALLED_APPS = [
           ...
           'lernito_openedx',
           ...
       ]

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
