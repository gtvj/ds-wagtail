from django.conf import settings

from wagtail import blocks

from .paragraph import APIRichTextBlock


class DoDontBlock(blocks.StructBlock):
    text = APIRichTextBlock(features=settings.INLINE_RICH_TEXT_FEATURES)


class DoDontListBlock(blocks.StructBlock):
    do = blocks.ListBlock(DoDontBlock(icon="check", label="Do item"), label="Dos")
    dont = blocks.ListBlock(
        DoDontBlock(icon="cross", label="Don't item"), label="Don'ts"
    )

    class Meta:
        icon = "tasks"
        label = "Do/Don't List"
        template = "blocks/do-dont-list.html"
