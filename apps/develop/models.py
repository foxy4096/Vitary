from django.db import models

from django.contrib.auth.models import User
import uuid

class DevProfile(models.Model):
    """
    DevProfile model for developers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True)
    github_username = models.CharField(max_length=50, blank=True, null=True)
    twitter_username = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True, default="")
    public_key = models.CharField(max_length=50, blank=True, null=True)
    private_key = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        """
        String representation of the model
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Returns the absolute url to the profile
        """
        from django.urls import reverse
        return reverse('profile_view', kwargs={'username': self.user.username})

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name or self.user.username} {self.last_name or ''}"

    def to_json(self):
        """
        Returns a json representation of the model
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'bio': self.bio,
            'github_username': self.github_username,
            'twitter_username': self.twitter_username,
            'website': self.website,
        }


class DocumentationCategory(models.Model):
    """
    DocumentCategory model
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        verbose_name = "Documentation Category"
        verbose_name_plural = "Documentation Categories"

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class Documentation(models.Model):
    """
    Docs model
    """
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        DocumentationCategory, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date"]

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'content': self.content,
            'documentation_category': self.documentation_category.name,
            'date': self.date.strftime("%b %d, %Y %H:%M:%S"),
        }



class Bot(models.Model):
    """
    Bot model
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    private_key = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date"]

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.date.strftime("%b %d, %Y %H:%M:%S"),
            'endpoint': self.endpoint,
        }

class WebHook(models.Model):
    """
    WebHook model
    """
    REQUEST_TYPE_CHOICES = (
        ('GET', 'GET'),
        ('POST', 'POST'),
    )
    EVENT_TYPE = (
        ('on_vit_mention', 'On Vit Mention'),
        ('on_comment_mention', 'On Comment Mention'),
        ('on_follow', 'On Follow'),
        ('on_message', 'On Message'),
    )
    CONTENT_TYPE = (
        ('application/json', 'application/json'),
        ('application/x-www-form-urlencoded', 'application/x-www-form-urlencoded'),
    )
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, blank=True, null=True)
    payload_url = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE, blank=True, null=True)
    method = models.CharField(max_length=5, choices=REQUEST_TYPE_CHOICES, default='GET')
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE, default='application/json')
    date = models.DateTimeField(auto_now=True)
    required_authentication = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date"]

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.date.strftime("%b %d, %Y %H:%M:%S"),
            'url': self.url,
            'event_type': self.event_type,
            'method': self.method,
            'required_authentication': self.required_authentication,
        }