from django.db import models

from django.contrib.auth.models import User


class Feed(models.Model):
    """
    Feed model
    """
    body = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="feeds")
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/images/', blank=True,
                              null=True, help_text="You can upload upto one image per feed")
    video = models.FileField(upload_to='uploads/videos/', blank=True,
                             null=True, help_text="You can upload upto one video per feed")
    likes = models.ManyToManyField(User, related_name="liked_feeds")

    def __str__(self):
        return f"Feed No.{self.pk} by {self.user.username.title()}"

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.video.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('feed_detail', kwargs={'pk': self.pk})

    def latest_feeds():
        return Feed.objects.all().order_by('-date')[:5]

class FeedComment(models.Model):
    """
    Feed Commnet model"""
    body = models.TextField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment no.{self.pk} On {self.feed} By {self.user.username.title()}"

    class Meta:
        ordering = ['-date']
