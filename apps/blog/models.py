from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import User

class Post(models.Model):
    """
    A post model for blog app
    """
    title = models.CharField(max_length=255)
    sdesc = models.CharField(max_length=255, verbose_name="Short Description")
    body = models.TextField(verbose_name="Body")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    cover_img = models.ImageField(upload_to='blog/images', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(f"{self.title}-{self.pk}")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})
