from wagtail import blocks
from etna.core.blocks import APIImageChooserBlock


class PromotedLinkBlock(blocks.StructBlock):
    url = blocks.URLBlock(label="External URL", help_text="URL for the external page")
    title = blocks.CharBlock(max_length=100, help_text="Title of the promoted page")
    teaser_image = APIImageChooserBlock(
        help_text="Image that will appear on thumbnails and promos around the site."
    )
    description = blocks.CharBlock(
        max_length=200, help_text="A description of the promoted page"
    )


class AuthorPromotedLinkBlock(PromotedLinkBlock):
    publication_date = blocks.CharBlock(
        required=False,
        help_text="This is a free text field. Please enter date as per agreed format: 14 April 2021",
    )
    author = blocks.CharBlock(required=False)
