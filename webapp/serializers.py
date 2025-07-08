from rest_framework.serializers import ModelSerializer
from .models import Complaint
from .models import OnlineClass

class ComplaintSerializer(ModelSerializer):
    class Meta:
        model = Complaint
        fields ='__all__'

class StudentSerializer(ModelSerializer):
    class Meta:
        model = OnlineClass
        fields ='__all__'


from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    formatted_date = serializers.ReadOnlyField()
    tag_list = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content',
            'image_src', 'image_alt', 'meta_description', 'keywords',
            'og_title', 'og_description', 'og_image', 'og_url', 'og_type', 'og_site_name',
            'twitter_card', 'twitter_title', 'twitter_description', 'twitter_image', 
            'twitter_site', 'twitter_creator', 'published_date', 'read_time', 'tags',
            'is_published', 'is_featured', 'created_at', 'updated_at',
            'formatted_date', 'tag_list'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'formatted_date', 'tag_list']

class BlogPostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for blog list view"""
    formatted_date = serializers.ReadOnlyField()
    tag_list = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'image_src', 'image_alt',
            'published_date', 'read_time', 'tags', 'formatted_date', 'tag_list'
        ]