"""
Base blocks dan komponen dasar yang dipakai oleh semua model.
Tidak ada Page models di sini, hanya blocks.
"""
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


# ============================================================
#  BASE BLOCKS (Reusable)
# ============================================================

class HeroBlock(blocks.StructBlock):
    background = ImageChooserBlock(required=False)
    title = blocks.CharBlock()
    subtitle = blocks.TextBlock(required=False)

    class Meta:
        icon = "image"
        label = "Hero Section"


class SectionHeadingBlock(blocks.StructBlock):
    heading = blocks.CharBlock()

    class Meta:
        icon = "title"
        label = "Section Heading"


class ParagraphBlock(blocks.RichTextBlock):
    class Meta:
        icon = "doc-full"
        label = "Paragraph"


class TwoColumnBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    image_position = blocks.ChoiceBlock(
        choices=[("left", "Image Left"), ("right", "Image Right")],
        default="left"
    )

    class Meta:
        icon = "placeholder"
        label = "Two Column Layout"


class CardItemBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=False)
    title = blocks.CharBlock()
    body = blocks.TextBlock(required=False)

    class Meta:
        icon = "list-ul"
        label = "Card"


class CardGridBlock(blocks.StructBlock):
    items = blocks.ListBlock(CardItemBlock())

    class Meta:
        icon = "table"
        label = "Card Grid"


class NumberedListBlock(blocks.StructBlock):
    items = blocks.ListBlock(blocks.CharBlock())

    class Meta:
        icon = "list-ol"
        label = "Numbered List"


class GalleryBlock(blocks.StructBlock):
    images = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        icon = "image"
        label = "Image Gallery"


class RawHTMLBlock(blocks.RawHTMLBlock):
    class Meta:
        icon = "code"
        label = "Custom HTML"


# List of common blocks untuk StreamField
COMMON_BLOCKS = [
    ("hero", HeroBlock()),
    ("section_heading", SectionHeadingBlock()),
    ("paragraph", ParagraphBlock()),
    ("two_columns", TwoColumnBlock()),
    ("card_grid", CardGridBlock()),
    ("numbered_list", NumberedListBlock()),
    ("gallery", GalleryBlock()),
    ("html", RawHTMLBlock()),
]