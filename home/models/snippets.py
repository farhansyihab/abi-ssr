"""
Snippet models untuk kategori, tags, dll.
"""
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel


@register_snippet
class ArticleCategory(models.Model):
    """Snippet sederhana untuk kategori artikel"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategori Artikel"
        verbose_name_plural = "Kategori Artikel"
        ordering = ['name']