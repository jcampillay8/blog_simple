from django.db import models
from django.contrib.auth.models import User
from django.db.models import base
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField
from django.utils import timezone


class Catogory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    options =   (
        ('draft','Draft'),
        ('published','Published'),
    )

    category = models.ForeignKey(Catogory, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=255) 
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published', null=False, unique=True)
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=options, default='draft')
    object = models.Manager() # default manager
    postobjects = PostObjects() # default manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ("publish",)

        def __str__(self):
            return f"Comment by {self.name}"