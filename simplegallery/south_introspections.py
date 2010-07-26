from south.modelsinspector import add_introspection_rules
from tinymce.models import HTMLField
from django.conf import settings
from django.db.models.fields import NOT_PROVIDED


rules = [
            (
                (HTMLField, ),
                [],
                {"null": ["null", {"default": False}],
                "blank": ["blank", {"default": False, "ignore_if":"primary_key"}],
                "primary_key": ["primary_key", {"default": False}],
                "max_length": ["max_length", {"default": None}],
                "unique": ["_unique", {"default": False}],
                "db_index": ["db_index", {"default": False}],
                "default": ["default", {"default": NOT_PROVIDED}],
                "db_column": ["db_column", {"default": None}],
                "db_tablespace": ["db_tablespace", {"default": settings.DEFAULT_INDEX_TABLESPACE}],
                },
            ),
        ]

add_introspection_rules(rules, ["^tinymce\.models\.HTMLField$"])