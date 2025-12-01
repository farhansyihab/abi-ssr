# home/api.py
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from wagtail.models import Page
from .models import HomePage

# Serializer untuk Page
class PageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'url', 'first_published_at']
    
    def get_url(self, obj):
        return obj.get_full_url()

# Serializer khusus untuk HomePage
class HomePageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = HomePage
        fields = ['id', 'title', 'slug', 'url', 'body']
    
    def get_url(self, obj):
        return obj.get_full_url()

# API ViewSet
class PageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.live().public()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        page_type = self.request.query_params.get('type', None)
        
        if page_type == 'home':
            queryset = queryset.type(HomePage)
        
        return queryset

class HomePageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HomePageSerializer
    queryset = HomePage.objects.live().public()