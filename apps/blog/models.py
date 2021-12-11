from django.db import models
from django.utils.text import slugify

from apps.accounts.models import Profile


class Post(models.Model):
    title = models.CharField(max_length=255)
    sdesc = models.CharField(max_length=255, verbose_name="Short Description")
    body = models.TextField(verbose_name="Body")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    cover_img = models.ImageField(upload_to='blog/imgs', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(self, *args, **kwargs)

    class Meta:
        ordering = ['-date']
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})