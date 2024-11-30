"""
lernito_openedx Django application initialization.
"""

from django.apps import AppConfig

# defined here for importing
app_name = "lernito_openedx"
app_name_verbose = "Lernito OpenedX"


class LernitoOpenedxConfig(AppConfig):
    """
    Configuration for the lernito_openedx Django application.
    """

    name = app_name
    verbose_name = app_name_verbose

    # Configure the app as a Plugin App
    plugin_app = {
        "url_config": {
            "lms.djangoapp": {
                "namespace": "lernito",
                "regex": "^lernito/",
                "relative_path": "urls",
            },
            "cms.djangoapp": {
                "namespace": "lernito",
                "regex": "^lernito/",
                "relative_path": "urls",
            },
        },
        # Add basic settings configuration
        "settings_config": {
            "lms.djangoapp": {
                "common": {"relative_path": "settings.common"},
            },
            "cms.djangoapp": {
                "common": {"relative_path": "settings.common"},
            },
        },
    }

    def ready(self):
        """
        Connect handlers to signals if needed.
        """
        pass
