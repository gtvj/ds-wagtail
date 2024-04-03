from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

from wagtail import blocks
from wagtail.blocks import StructValue
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.blocks import ImageChooserBlock

from etna.core.blocks.paragraph import APIRichTextBlock


class APIImageChooserBlock(ImageChooserBlock):
    """
    APIImageChooserBlock inherits ImageChooserBlock and adds the ability
    to generate different renditions for JPEG and WebP formats. Without
    this, and the get_api_representation override, the API would return
    the database entry - which is just an image ID. This would require
    a second API call to get the image renditions.

    rendition_size defaults to `fill-600x400`, but can be specified
    when the block is used, e.g:
    image = APIImageChooserBlock(rendition_size="original")

    jpeg_quality and webp_quality default to 60 and 80 respectively,
    and can be specified in the same way as rendition_size.
    """

    def __init__(
        self,
        required=True,
        help_text=None,
        rendition_size="fill-600x400",
        jpeg_quality=60,
        webp_quality=80,
        **kwargs,
    ):
        self.jpeg_quality = jpeg_quality
        self.webp_quality = webp_quality
        self.rendition_size = rendition_size
        super().__init__(required=required, help_text=help_text, **kwargs)

    def get_api_representation(self, value, context=None):
        if value:
            jpeg_image = value.get_rendition(
                f"{self.rendition_size}|format-jpeg|jpegquality-{self.jpeg_quality}"
            )
            webp_image = value.get_rendition(
                f"{self.rendition_size}|format-webp|webpquality-{self.webp_quality}"
            )

            return {
                "id": value.id,
                "title": value.title,
                "image_jpeg": {
                    "url": jpeg_image.url,
                    "full_url": jpeg_image.full_url,
                    "width": jpeg_image.width,
                    "height": jpeg_image.height,
                },
                "image_webp": {
                    "url": webp_image.url,
                    "full_url": webp_image.full_url,
                    "width": webp_image.width,
                    "height": webp_image.height,
                },
                "transcript": (
                    {
                        "heading": value.get_transcription_heading_display(),
                        "text": value.transcription,
                    }
                    if value.transcription
                    else None
                ),
                "translation": (
                    {
                        "heading": value.get_translation_heading_display(),
                        "text": value.translation,
                    }
                    if value.translation
                    else None
                ),
            }
        return None


class ImageBlock(blocks.StructBlock):
    """
    An image block which allows editors to ensure accessibility is reflected on the page.
    """

    image = APIImageChooserBlock(required=True)
    decorative = blocks.BooleanBlock(
        label=mark_safe(
            "Is this image decorative? <p class='field-title__subheading'>Tick the box if 'yes'</p>"
        ),
        help_text=mark_safe(
            "Decorative images are used for visual effect and do not add information to the content of a page. "
            '<a href="https://www.w3.org/WAI/tutorials/images/decorative/" target="_blank">"Check the guidance to '
            "see if your image is decorative</a>."
        ),
        required=False,
        default=False,
    )

    alt_text = blocks.CharBlock(
        max_length=100,
        label="Image alternative text",
        help_text=mark_safe(
            "Alternative (alt) text describes images when they fail to load, and is read aloud by assistive "
            "technologies. Use a maximum of 100 characters to describe your image. Decorative images do not "
            'require alt text. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">'
            "Check the guidance for tips on writing alt text</a>."
        ),
        required=False,
    )

    caption = APIRichTextBlock(
        features=["bold", "italic", "link"],
        help_text=(
            "An optional caption for non-decorative images, which will be displayed directly below the image. "
            "This could be used for image sources or for other useful metadata."
        ),
        label="Caption (optional)",
        required=False,
    )

    def clean(self, value):
        image = value.get("image")
        decorative = value.get("decorative")
        alt_text = value.get("alt_text")
        caption = value.get("caption")

        errors = {}
        if image:
            if not decorative and not alt_text:
                message = "Non-decorative images must contain alt text."
                errors["alt_text"] = ErrorList([message])

            if decorative and alt_text:
                message = "Decorative images should not contain alt text."
                errors["alt_text"] = ErrorList([message])

            if decorative and caption:
                message = """Decorative images should not
                contain a caption to prevent confusing users of assistive technologies."""
                errors["caption"] = ErrorList([message])

        if errors:
            raise StructBlockValidationError(errors)

        return super().clean(value)

    class Meta:
        label = "Image"
        template = "blocks/image-block-default.html"
        help_text = "An image block which allows editors to ensure accessibility is reflected on the page."
        icon = "image"
        form_template = "form_templates/default-form-with-safe-label.html"


class NoCaptionImageBlock(ImageBlock):
    caption = None


class ImageOrientationValue(StructValue):
    def is_portrait(self):
        image = self.get("image")
        if image:
            return image.width < image.height


class ContentImageBlock(blocks.StructBlock):
    image = APIImageChooserBlock(rendition_size="max-900x900", required=True)
    alt_text = blocks.CharBlock(
        max_length=100,
        label="Alternative text",
        help_text=mark_safe(
            "Alternative (alt) text describes images when they fail to load, and is read aloud by assistive "
            "technologies. Use a maximum of 100 characters to describe your image. "
            '<a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">'
            "Check the guidance for tips on writing alt text</a>."
        ),
    )
    caption = APIRichTextBlock(
        features=["bold", "italic", "link"],
        help_text=(
            "If provided, displays directly below the image. Can be used to specify sources, transcripts or "
            "other useful metadata."
        ),
        label="Caption (optional)",
        required=False,
    )

    class Meta:
        label = "Image"
        template = "blocks/content_image.html"
        icon = "image"
        form_template = "form_templates/default-form-with-safe-label.html"
        value_class = ImageOrientationValue
