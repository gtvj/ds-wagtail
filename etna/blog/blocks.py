from django.core.exceptions import ValidationError

from wagtail import blocks

from etna.core.blocks import (
    ContactBlock,
    ContentImageBlock,
    ContentTableBlock,
    DocumentsBlock,
    ImageGalleryBlock,
    ParagraphBlock,
    QuoteBlock,
    SectionDepthAwareStructBlock,
    SubHeadingBlock,
    YouTubeBlock,
)

from ..media.blocks import MediaBlock


class SectionContentBlock(blocks.StreamBlock):
    contact = ContactBlock()
    document = DocumentsBlock()
    image = ContentImageBlock()
    image_gallery = ImageGalleryBlock()
    media = MediaBlock()
    paragraph = ParagraphBlock()
    quote = QuoteBlock()
    sub_heading = SubHeadingBlock()
    table = ContentTableBlock()
    youtube_video = YouTubeBlock()


class ContentSectionBlock(SectionDepthAwareStructBlock):
    heading = blocks.CharBlock(max_length=100, label="Heading")
    content = SectionContentBlock(required=False)

    class Meta:
        label = "Section"
        template = "articles/blocks/section.html"


class BlogPostPageStreamBlock(blocks.StreamBlock):
    """
    A block for the GeneralPage model.
    """

    content_section = ContentSectionBlock()
