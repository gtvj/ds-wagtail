from django.conf import settings
from django.urls import include, path, re_path, register_converter
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from etna.search import views as search_views
from etna.records import converters
from etna.records import views as records_views

register_converter(converters.ReferenceNumberConverter, "reference_number")

# fmt: off
urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),

    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),

    re_path(
        r"catalogue/(?P<iaid>C\d+)/",
        records_views.record_page_view,
        name="details-page-machine-readable",
    ),
    path(
        r"catalogue/<reference_number:reference_number>/",
        records_views.record_page_disambiguation_view,
        name="details-page-human-readable",
    ),
    path(
        r"catalogue/<reference_number:reference_number>/~<int:pseudo_reference>/",
        records_views.record_page_disambiguation_view,
        name="details-page-human-readable-with-pseudo-reference",
    ),
]
# fmt: on


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
