from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.utils.text import slugify

class DevProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    twitter_handle = models.CharField(max_length=100, blank=True)
    github_handle = models.CharField(max_length=100, blank=True)
    linkedin_handle = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

class DocumentationTag(models.Model):
    """
    The name of the tag.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(DocumentationTag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('documentation_tag', kwargs={'tag': self.slug})


class Documentation(models.Model):
    """
    Documentation model, used to store API documentation
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(DocumentationTag, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('documentation_detail', kwargs={'tag': self.tag.slug, 'title': self.slug})


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']