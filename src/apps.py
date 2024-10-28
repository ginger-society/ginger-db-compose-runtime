# pylint: disable=C0115
"""App definition for the src app"""

from gingerdj.apps import AppConfig


class SrcConfig(AppConfig):
    default_auto_field = "gingerdj.db.models.BigAutoField"
    name = "src"
