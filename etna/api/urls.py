from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import redirect
from django.utils.crypto import constant_time_compare

from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.utils import get_object_detail_url
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.models import Page, PageViewRestriction, Site

from rest_framework import status
from rest_framework.response import Response
from wagtail_headless_preview.models import PagePreview
from wagtailmedia.api.views import MediaAPIViewSet

from etna.core.serializers.pages import DefaultPageSerializer


class CustomPagesAPIViewSet(PagesAPIViewSet):
    def listing_view(self, request):
        queryset = self.get_queryset()
        self.check_query_parameters(queryset)
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = DefaultPageSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    meta_fields = PagesAPIViewSet.meta_fields + [
        "privacy",
        "latest_revision_created_at",
    ]


class PagePreviewAPIViewSet(PagesAPIViewSet):
    known_query_parameters = PagesAPIViewSet.known_query_parameters.union(
        ["content_type", "token"]
    )

    def listing_view(self, request):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def detail_view(self, request, pk):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def get_object(self):
        app_label, model = self.request.GET["content_type"].split(".")
        content_type = ContentType.objects.get(app_label=app_label, model=model)

        page_preview = PagePreview.objects.get(
            content_type=content_type, token=self.request.GET["token"]
        )
        page = page_preview.as_page()
        if not page.pk:
            # fake primary key to stop API URL routing from complaining
            page.pk = 0

        return page


class PrivatePageAPIViewSet(PagesAPIViewSet):
    known_query_parameters = PagesAPIViewSet.known_query_parameters.union(["password"])

    meta_fields = PagesAPIViewSet.meta_fields + [
        "privacy",
        "latest_revision_created_at",
    ]

    def get_base_queryset(self):
        queryset = Page.objects.all().live()
        if site := Site.find_for_request(self.request):
            base_queryset = queryset
            return base_queryset.descendant_of(site.root_page, inclusive=True)
        else:
            return queryset.none()

    def detail_view(self, request, pk):
        instance = self.get_object()
        restrictions = instance.get_view_restrictions()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if not restrictions:
            return Response(data)
        for restriction in restrictions:
            if restriction.restriction_type == PageViewRestriction.PASSWORD:
                if "password" in request.GET:
                    if constant_time_compare(
                        request.GET["password"], restriction.password
                    ):
                        return Response(data)
                    else:
                        data = {"message": "Incorrect password."}
                        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    data = {"message": "Password required to view this resource."}
                    return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        data = {"message": "Selected privacy is not compatible with this API."}
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    def find_view(self, request):
        queryset = self.get_queryset()
        try:
            obj = self.find_object(queryset, request)
            if obj is None:
                raise self.model.DoesNotExist
        except self.model.DoesNotExist:
            raise Http404("not found")
        url = get_object_detail_url(
            self.request.wagtailapi_router, request, self.model, obj.pk
        )
        if url is None:
            # Shouldn't happen unless this endpoint isn't actually installed in the router
            raise Exception(
                "Cannot generate URL to detail view. Is '{}' installed in the API router?".format(
                    self.__class__.__name__
                )
            )
        if "password" in request.GET:
            url = f"{url}?password={request.GET["password"]}"
        return redirect(url)

    name = "private_pages"


class CustomImagesAPIViewSet(ImagesAPIViewSet):
    body_fields = ImagesAPIViewSet.body_fields + [
        "title",
        "file",
        "copyright",
        "is_sensitive",
        "custom_sensitive_image_warning",
        "tags",
        "transcription_heading",
        "transcription",
        "translation_heading",
        "translation",
        "record",
        "record_dates",
        "description",
    ]


api_router = WagtailAPIRouter("wagtailapi")

api_router.register_endpoint("private_pages", PrivatePageAPIViewSet)
api_router.register_endpoint("pages", CustomPagesAPIViewSet)
api_router.register_endpoint("page_preview", PagePreviewAPIViewSet)
api_router.register_endpoint("images", CustomImagesAPIViewSet)
api_router.register_endpoint("media", MediaAPIViewSet)
