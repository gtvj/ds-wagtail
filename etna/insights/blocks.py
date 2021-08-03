from wagtail.core import blocks

from ..quotes.blocks import QuoteBlock
from ..paragraphs.blocks import ParagraphWithHeading
from ..media.blocks import MediaBlock, EtnaMediaBlock


class InsightsPageStreamBlock(blocks.StreamBlock):
    quote = QuoteBlock()
    paragraph_with_heading = ParagraphWithHeading()
    media = EtnaMediaBlock()
