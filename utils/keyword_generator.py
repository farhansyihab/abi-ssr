# utils/keyword_generator.py

import re
from collections import Counter

class KeywordGenerator:
    """Generate relevant keywords dari konten artikel"""
    
    # Stopwords Bahasa Indonesia
    INDONESIAN_STOPWORDS = {
        'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dengan', 
        'adalah', 'atau', 'ini', 'itu', 'dalam', 'tidak', 'akan', 
        'kepada', 'oleh', 'saat', 'juga', 'bisa', 'ada', 'mereka',
        'kami', 'kita', 'saya', 'anda', 'dia', 'mereka', 'serta',
        'namun', 'tetapi', 'melalui', 'terhadap', 'sebagai', 'jika',
        'karena', 'maka', 'pernah', 'harus', 'sangat', 'lebih',
        'telah', 'sedang', 'nanti', 'lagi', 'perlu', 'boleh',
        'sudah', 'masih', 'rata', 'sama', 'hanya', 'cukup',
        'begitu', 'sambil', 'sekali', 'mau', 'mungkin',
    }
    
    @classmethod
    def extract_from_html(cls, html_content, max_keywords=10):
        """Extract keywords dari HTML content"""
        # 1. Strip HTML tags
        text = re.sub(r'<[^>]+>', ' ', html_content)
        
        # 2. Decode HTML entities
        import html
        text = html.unescape(text)
        
        # 3. Get words (min 3 characters)
        words = re.findall(r'\b\w{3,}\b', text.lower())
        
        # 4. Remove stopwords
        keywords = [w for w in words if w not in cls.INDONESIAN_STOPWORDS]
        
        # 5. Count frequency
        word_counts = Counter(keywords)
        
        # 6. Get top keywords
        top_keywords = [word for word, count in word_counts.most_common(max_keywords)]
        
        return ', '.join(top_keywords)
    
    @classmethod
    def generate_for_article(cls, article):
        """Generate keywords untuk artikel"""
        # Extract dari title
        title_keywords = cls.extract_from_text(article.title, 3)
        
        # Extract dari excerpt
        excerpt_keywords = cls.extract_from_text(article.excerpt or '', 2)
        
        # Extract dari HTML content
        html_content = cls.get_html_content(article)
        content_keywords = cls.extract_from_html(html_content, 5)
        
        # Combine
        all_keywords = set()
        for kw_list in [title_keywords, excerpt_keywords, content_keywords]:
            if kw_list:
                all_keywords.update(kw_list.split(', '))
        
        return ', '.join(list(all_keywords)[:10])  # Max 10 keywords
    
    @classmethod
    def extract_from_text(cls, text, max_words=5):
        """Extract keywords dari plain text"""
        if not text:
            return ''
        
        words = re.findall(r'\b\w{3,}\b', text.lower())
        keywords = [w for w in words if w not in cls.INDONESIAN_STOPWORDS]
        
        return ', '.join(keywords[:max_words])
    
    @classmethod
    def get_html_content(cls, article):
        """Extract HTML dari StreamField body"""
        html_parts = []
        
        for block in article.body:
            if block.block_type == 'html':
                html_parts.append(block.value)
        
        return ' '.join(html_parts)
