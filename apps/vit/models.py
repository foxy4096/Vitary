from django.db import models

from django.contrib.auth.models import User

class Vit(models.Model):
    """
    Vit model
    """

    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vits")
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to="uploads/images/",
        blank=True,
        null=True,
        help_text="You can upload upto one image per Vit",
    )
    video = models.FileField(
        upload_to="uploads/videos/",
        blank=True,
        null=True,
        help_text="You can upload upto one video per Vit"
    )
    likes = models.ManyToManyField(User, related_name="liked_vits")
    like_count = models.IntegerField(default=0)
    plustag = models.ManyToManyField("Plustag", blank=True)
    mentions = models.ManyToManyField(User, related_name="mentioned_vits")
    nsfw = models.BooleanField("Is the Content NSFW?", default=False, help_text="Mark as NSFW if the content is not safe for work")
    

    def save(self, *args, **kwargs):
        self.body = self.body.strip()
        super().save(*args, **kwargs)
        for plus in self.plustag.all():
            plus.rating = plus.vit_set.count()
            plus.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vit No.{self.pk}"


    class Meta:
        ordering = ["-date"]

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("vit_detail", kwargs={"pk": self.pk})

    def latest_vits():
        return Vit.objects.all().order_by("-like_count", "-date")[:5]

    def to_json(self):
        return {
            "id": self.id,
            "body": self.body,
            "user": self.user.username,
            "date": self.date.strftime("%b %d, %Y %H:%M:%S"),
            "image": self.image.url if self.image else None,
            "video": self.video.url if self.video else None,
            "likes": self.likes.count(),
            "plustag": [plus.name for plus in self.plustag.all()],
            "mentions": [mention.profile.user.username for mention in self.mentions.all()],
            "nsfw": self.nsfw,
        }

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
    vit = models.ForeignKey(Vit, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username.title()}"

    class Meta:
        ordering = ["-date"]


class Embed(models.Model):
    """
    Embed model
    """

    url = models.URLField()
    vit = models.ForeignKey(Vit, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    

    def __str__(self):
        return f"Embed {self.url}"
