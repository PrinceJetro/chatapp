from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime  import datetime



class User(AbstractUser):
    avatar = models.ImageField(null=True)
    image_link = models.TextField(max_length=1000, null=True)
    REQUIRED_FIELDS = []
    

class Complaint(models.Model):
     categories = models.CharField(max_length=2000)
     body = models.TextField(max_length=10000)
     img = models.ImageField(max_length=5000, null=True)
     image_link = models.TextField(max_length=5000, null=True)
     def __str__(self):
         return self.categories


class OnlineClass(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)  # Changed to CharField
    more = models.TextField()

    def __str__(self):
        return self.full_name



from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class BlogPost(models.Model):
    # Basic Information
    title = models.CharField(max_length=200, help_text="Blog post title")
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text="URL-friendly version of title")
    excerpt = models.TextField(max_length=500, help_text="Short description for blog list")
    content = models.TextField(help_text="Full blog post content (HTML allowed)")
    
    # Media
    image_src = models.CharField(max_length=255, help_text="Path to blog cover image (e.g., 'blogimages/blog1.png')")
    image_alt = models.CharField(max_length=200, help_text="Alt text for blog cover image")
    
    # Meta Information
    meta_description = models.TextField(max_length=300, help_text="SEO meta description")
    keywords = models.CharField(max_length=500, blank=True, help_text="SEO keywords (comma-separated)")
    
    # Social Media Meta Tags
    og_title = models.CharField(max_length=200, blank=True, help_text="Open Graph title")
    og_description = models.TextField(max_length=300, blank=True, help_text="Open Graph description")
    og_image = models.URLField(blank=True, help_text="Full URL to Open Graph image")
    og_url = models.URLField(blank=True, help_text="Full URL to this blog post")
    og_type = models.CharField(max_length=50, default="article", help_text="Open Graph type")
    og_site_name = models.CharField(max_length=100, default="Jephthah Adegbuyi", help_text="Open Graph site name")
    
    # Twitter Meta Tags
    twitter_card = models.CharField(max_length=50, default="summary_large_image", help_text="Twitter card type")
    twitter_title = models.CharField(max_length=200, blank=True, help_text="Twitter title")
    twitter_description = models.TextField(max_length=300, blank=True, help_text="Twitter description")
    twitter_image = models.URLField(blank=True, help_text="Full URL to Twitter image")
    twitter_site = models.CharField(max_length=100, default="@princejetro123", help_text="Twitter site handle")
    twitter_creator = models.CharField(max_length=100, default="@princejetro123", help_text="Twitter creator handle")
    
    # Publishing Information
    published_date = models.DateTimeField(default=timezone.now, help_text="Publication date")
    read_time = models.CharField(max_length=20, help_text="Estimated read time (e.g., '7 min')")
    tags = models.CharField(max_length=500, blank=True, help_text="Tags for the blog post (e.g., '#SmallBusiness #Marketing')")
    
    # Status
    is_published = models.BooleanField(default=True, help_text="Whether the post is published")
    is_featured = models.BooleanField(default=False, help_text="Whether to feature this post")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-fill social media fields if not provided
        if not self.og_title:
            self.og_title = self.title
        if not self.og_description:
            self.og_description = self.meta_description
        if not self.twitter_title:
            self.twitter_title = self.title
        if not self.twitter_description:
            self.twitter_description = self.meta_description
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    @property
    def formatted_date(self):
        """Return formatted date for display"""
        return self.published_date.strftime("%B %d, %Y")
    
    @property
    def tag_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split('#') if tag.strip()]
        return []
    


