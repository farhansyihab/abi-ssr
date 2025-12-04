# home/models/__init__.py
# Import semua model dari submodules dengan error handling

try:
    from .base import *
except ImportError as e:
    print(f"Warning: Could not import from base: {e}")

try:
    from .pages import *
except ImportError as e:
    print(f"Warning: Could not import from pages: {e}")

try:
    from .articles import *
except ImportError as e:
    print(f"Warning: Could not import from articles: {e}")

try:
    from .snippets import *
except ImportError as e:
    print(f"Warning: Could not import from snippets: {e}")

# Django butuh ini untuk menemukan models
__all__ = [
    # Base blocks
    'HeroBlock', 'SectionHeadingBlock', 'ParagraphBlock', 'TwoColumnBlock',
    'CardItemBlock', 'CardGridBlock', 'NumberedListBlock', 'GalleryBlock',
    'RawHTMLBlock', 'COMMON_BLOCKS',
    
    # Page models
    'StandardPage', 'HomePage',
    
    # Article models
    'ArticlePage', 'ArticleIndexPage',
    
    # Snippets
    'ArticleCategory',
]