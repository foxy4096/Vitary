from django.db import models

from django.utils.safestring import mark_safe
import secrets
from django_resized import ResizedImageField

from django.contrib.auth.models import User
from apps.core.models import Badge
from django.conf import settings

class Profile(models.Model):
    """
    Extending the base user model
    """

    STATUS = (("online", "Online"), ("away", "Away"), ("colorful", "Colorful"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ResizedImageField(
        size=[600, 600], crop=["middle", "center"],
        upload_to="uploads/",
        default="/uploads/default.jpg",
        verbose_name="Profile Image",
    )
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False
    )
    follower_count = models.IntegerField(default=0, editable=False)
    following_count = models.IntegerField(default=0, editable=False)
    email_notif = models.BooleanField(
        default=True, verbose_name="Get Email Notifications"
    )
    verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True, null=True, default="")
    header_image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    badges = models.ManyToManyField(Badge, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default="online")
    allow_nsfw = models.BooleanField("Allow NSFW Content", default=False)
    auth_token = models.CharField(max_length=100, blank=True, null=True)

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

        return reverse("user_detail", kwargs={"username": self.user.username})

    def get_4_followers(self):
        """
        Returns the 4 most recent followers
        """
        return self.follows.all()[:4]

    def get_4_following(self):
        """
        Returns the 4 most recent follows
        """
        return self.followed_by.all()[:4]

    def profile_image(self):
        """
        Returns the profile image
        """
        return mark_safe(
            f'<img src="{self.image.url}" height=100px / style="border-radius: 10%">'
        )

    def to_json(self):
        """
        Returns a json representation of the model
        """
        return {
            "id": self.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "bio": self.bio,
            "image": f"{settings.WEB_HOST}{self.image.url}" if self.image else None,
            "header_image": f"{settings.WEB_HOST}{self.header_image.url}" if self.header_image else None,
            "follower_count": self.follower_count,
            "following_count": self.following_count,
            "verified": self.verified,
            "allow_nsfw": self.allow_nsfw,
        }

    def get_auth_token(self):
        if self.auth_token is None:
            self.auth_token = secrets.token_hex(16)
            self.save()
        return self.auth_token
