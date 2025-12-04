"""
Page models untuk halaman regular (non-artikel).
"""
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image

from .base import COMMON_BLOCKS


# ============================================================
#  STANDARD PAGE
# ============================================================

class StandardPage(Page):
    template = "home/content_page.html"

    body = StreamField(
        COMMON_BLOCKS,
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