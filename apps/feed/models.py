from django.db import models
from django.contrib.auth.models import User
from apps.notification.utilities import create_notification


class Feed(models.Model):
    """
    feed model
    """

    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feeds")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_feeds", blank=True)
    like_count = models.IntegerField(default=0)
    plustag = models.ManyToManyField("Plustag", blank=True)
    mentions = models.ManyToManyField(User, related_name="mentioned_feeds", blank=True)
    image = models.ImageField(
        upload_to="uploads/images/",
        blank=True,
        null=True,
        help_text="You can upload upto one image per feed",
    )
    video = models.FileField(
        upload_to="uploads/videos/",
        blank=True,
        null=True,
        help_text="You can upload upto one video per feed",
    )
    nsfw = models.BooleanField(
        default=False,
        help_text="Contains mature or adult content",
        verbose_name="Not Safe For Work (NSFW)",
    )

    class Meta:
        ordering = ["-date"]

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("feed_detail", kwargs={"pk": self.pk})

    def like_feed(self, user: User):
        if user in self.likes.all():
            self.likes.remove(user)
            self.like_count -= 1
        else:
            self.likes.add(user)
            self.like_count += 1
            create_notification(
                recipient=self.user,
                actor=user,
                object_type="feed",
                verb="like",
                object_id=self.id,
            )

        self.save()

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.video.delete()
        super().delete(*args, **kwargs)

    def latest_feeds():
        return Feed.objects.all().order_by("-like_count", "-date")[:5]


class Plustag(models.Model):
    """
    Plustag model
    """

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True, null=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-rating"]


class Comment(models.Model):
    """
    Comment model
    """

    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="replies"
    )
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment {self.id} by {self.user.username.title()}"

    class Meta:
        ordering = ["-date"]
