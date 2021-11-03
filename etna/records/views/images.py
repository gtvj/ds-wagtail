from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import Http404, render
from django.views.decorators.cache import cache_control

from ...ciim.exceptions import (
    DoesNotExist,
    InvalidQuery,
    KongException,
    UnsupportedSlice,
)
from ...ciim.utils import convert_sort_key_to_index
from ..models import Image, RecordPage


def image_viewer(request, iaid, sort):
    """View to render a single image for a record."""

    try:
        page = RecordPage.search.get(iaid)
    except DoesNotExist:
        raise Http404

    if not page.is_digitised:
        raise Http404

    try:
        images = Image.search.filter(rid=page.media_reference_id)
    except InvalidQuery:
        # Raised if the RecordPage doesn't have a media_reference_id
        raise Http404

    # Sort key generated by CIIM is prefixed by a number to avoid issues
    # when sorting alphabetically, i.e ordering 1 , 11, 2 instead of 1, 2, 11
    # convert to index to use as offset in a Kong query
    index = convert_sort_key_to_index(sort)

    try:
        previous_image = images[index - 1]
    except UnsupportedSlice:
        # Attempted to fetch using a negative index meaning we're viewing the
        # first image and therefore there's no previous image to fetch.
        previous_image = None
    except KongException:
        # Subscripting for the previous image will trigger a request to Kong.
        # If the query isn't valid, this is where the exception will be raised..
        raise Http404

    try:
        image = images[index]
    except IndexError:
        raise Http404

    try:
        next_image = images[index + 1]
    except IndexError:
        next_image = None

    return render(
        request,
        "records/image-viewer.html",
        {
            "page": page,
            "image": image,
            "images": images,
            "index": index,
            "next_image": next_image,
            "previous_image": previous_image,
        },
    )


def image_browse(request, iaid):
    try:
        page = RecordPage.search.get(iaid)
    except DoesNotExist:
        raise Http404

    if not page.is_digitised:
        raise Http404

    try:
        images = Image.search.filter(rid=page.media_reference_id)
    except InvalidQuery:
        # Raised if the RecordPage doesn't have a media_reference_id
        raise Http404

    page_number = request.GET.get("page", 1)
    paginator = Paginator(images, 20)
    images = paginator.get_page(page_number)

    return render(
        request,
        "records/image-browse.html",
        {
            "page": page,
            "images": images,
            # Obtaining the count requires a network request.
            # Pass the value to the template to prevent
            # unexpected performance issues
            "images_count": paginator.count,
        },
    )


# Cache assets for a day or indefinitely if browser supports it
@cache_control(max_age="259200", public=True, immutable=True)
def image_serve(request, location):
    """Relay content served from Kong's /media endpoint"""
    response = Image.media.serve(location)

    if not response.ok:
        raise Http404

    return FileResponse(
        response.raw,
        content_type="image/jpeg",
        reason=response.reason,
    )
