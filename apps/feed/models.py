from django.db import models

from apps.accounts.models import Profile


class Feed(models.Model):
    body = models.TextField()
    created_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="feeds")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='uploads/images/', blank=True,
                              null=True, help_text="You can upload upto one image per feed")
    video = models.FileField(upload_to='uploads/videos/', blank=True,
                             null=True, help_text="You can upload upto one video per feed")
    likes = models.ManyToManyField(Profile, related_name="liked_feeds")

    def __str__(self):
        return f"Feed No.{self.pk} by {self.created_by.user.username.title()}"

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.video.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_on']


class FeedComment(models.Model):
    body = models.TextField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment no.{self.pk} On {self.feed} By {self.created_by.user.username.title()}"

    class Meta:
        ordering = ['-created_on']
