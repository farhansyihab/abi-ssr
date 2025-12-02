from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image


# ============================================================
#  STANDARD PAGE
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


class StandardPage(Page):
    template = "home/content_page.html"

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("section_heading", SectionHeadingBlock()),
            ("paragraph", ParagraphBlock()),
            ("two_columns", TwoColumnBlock()),
            ("card_grid", CardGridBlock()),
            ("numbered_list", NumberedListBlock()),
            ("gallery", GalleryBlock()),
            ("html", RawHTMLBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


# ============================================================
#  HOME PAGE
# ============================================================

class HomePage(Page):
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_button_text = models.CharField(max_length=100, blank=True)
    hero_button_link = models.URLField(blank=True)
    hero_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    template = "home/home_page.html"

    content_panels = Page.content_panels + [
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_button_text"),
        FieldPanel("hero_button_link"),
        FieldPanel("hero_image"),
    ]
