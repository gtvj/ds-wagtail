from django.templatetags.static import static
from django.utils.html import format_html
from django.conf import settings

from wagtail.core import hooks


@hooks.register("insert_editor_css")
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/dist/etna-wagtail-editor.css")
    )

@hooks.register('insert_global_admin_css')
def global_admin_css():
    if settings.FEATURE_PLATFORM_ENVIRONMENT_TYPE in ["development", "staging"]:
        return '<style> :root {--w-color-primary: #104100; --w-color-primary-200: #103200;} </style>'
    return ""