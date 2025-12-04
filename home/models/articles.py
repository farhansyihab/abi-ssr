"""
Article/Blog system models.
"""
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from wagtail.search import index

from .base import ParagraphBlock, TwoColumnBlock, CardGridBlock, GalleryBlock, RawHTMLBlock, NumberedListBlock


# ============================================================
#  ARTICLE / BLOG SYSTEM
# ============================================================

class ArticlePage(Page):
    """Model untuk artikel/berita dengan struktur standar Wagtail"""
    
    # Metadata dasar
    date_published = models.DateField("Tanggal Publikasi", null=True, blank=True)
    excerpt = models.TextField("Ringkasan", max_length=300, blank=True)
    featured_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Gambar Utama"
    )
    
    # Relasi sederhana (snippet) - String reference untuk hindari circular import
    category = models.ForeignKey(
        'home.ArticleCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles",
        verbose_name="Kategori"
    )
    
    # Konten utama menggunakan SUBSET dari common blocks
    body = StreamField(
        [
            ("paragraph", ParagraphBlock()),
            ("two_columns", TwoColumnBlock()),
            ("card_grid", CardGridBlock()),
            ("gallery", GalleryBlock()),
            ("html", RawHTMLBlock()),
            ("numbered_list", NumberedListBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Konten Artikel"
    )
    
    template = "home/article_detail.html"
    parent_page_types = ['home.ArticleIndexPage']
    subpage_types = []
    
    # Search configuration
    search_fields = Page.search_fields + [
        index.SearchField('excerpt'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('date_published'),
        FieldPanel('excerpt'),
        FieldPanel('featured_image'),
        FieldPanel('category'),
        FieldPanel('body'),
    ]
    
    # Promote panels untuk SEO
    promote_panels = [
        FieldPanel('slug'),
        FieldPanel('seo_title'),
        FieldPanel('search_description'),
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Artikel terbaru untuk sidebar
        # Gunakan sibling_of untuk artikel di index yang sama
        context['latest_articles'] = ArticlePage.objects.live()\
            .sibling_of(self)\
            .order_by('-date_published', '-first_published_at')\
            .exclude(id=self.id)[:5]
        
        # Fallback jika tidak ada sibling, ambil dari parent index
        if not context['latest_articles']:
            parent_index = self.get_parent().specific
            if hasattr(parent_index, 'get_articles'):
                context['latest_articles'] = parent_index.get_articles()\
                    .exclude(id=self.id)[:5]
        
        return context
    
    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikel"


class ArticleIndexPage(Page):
    """Halaman indeks untuk menampilkan daftar artikel"""
    
    template = "home/article_list.html"
    subpage_types = ['home.ArticlePage']
    
    # Pengaturan pagination
    articles_per_page = 10
    
    def get_articles(self):
        """Method helper untuk mendapatkan artikel"""
        return ArticlePage.objects.live().descendant_of(self)\
            .order_by('-date_published', '-first_published_at')
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all live articles
        articles = self.get_articles()
        
        # Filter by category jika ada
        category_id = request.GET.get('category')
        if category_id:
            articles = articles.filter(category_id=category_id)
        
        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(articles, self.articles_per_page)
        
        try:
            articles_page = paginator.page(page)
        except PageNotAnInteger:
            articles_page = paginator.page(1)
        except EmptyPage:
            articles_page = paginator.page(paginator.num_pages)
        
        # Get categories for sidebar - dengan error handling
        try:
            from .snippets import ArticleCategory
            context['categories'] = ArticleCategory.objects.all().order_by('name')
        except (ImportError, Exception) as e:
            # Fallback jika snippets belum ada atau error
            context['categories'] = []
            print(f"Warning: Could not load ArticleCategory: {e}")
        
        context['articles'] = articles_page
        context['current_category'] = category_id
        
        return context
    
    class Meta:
        verbose_name = "Indeks Artikel"
        verbose_name_plural = "Indeks Artikel"


# Export untuk __all__
__all__ = ['ArticlePage', 'ArticleIndexPage']