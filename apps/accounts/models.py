from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField
from django.utils.safestring import mark_safe
import secrets

from apps.core.models import Badge


class Profile(models.Model):
    """
    Extending the base user model
    """

    STATUS = (("online", "Online"), ("away", "Away"), ("colorful", "Colorful"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False
    )
    follower_count = models.IntegerField(default=0, editable=False)
    following_count = models.IntegerField(default=0, editable=False)
    email_notif = models.BooleanField(
        default=True, verbose_name="Get Email Notifications"
    )
    verified = models.BooleanField(default=False)
    bio = models.TextField(
        "About Yourself",
        max_length=500,
        blank=True,
        null=True,
        default="",
        help_text="Tell us about yourself",
    )
    header_image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    image = ResizedImageField(
        size=[600, 600],
        crop=["middle", "center"],
        upload_to="uploads/",
        default="/uploads/default.jpg",
        verbose_name="Profile Image",
    )
    badges = models.ManyToManyField(Badge, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default="online")
    date_of_birth = models.DateField(
        blank=True, null=True, help_text="It help to know when is your birthday"
    )

    allow_nsfw = models.BooleanField("Allow NSFW Content", default=False)

    auth_token = models.CharField(max_length=255, blank=True, null=True)

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

    def get_image_url(self):
        return self.image.url

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a token if one doesn't exist already.
        """
        if not self.auth_token:
            self.auth_token = secrets.token_hex(16)
        super().save(*args, **kwargs)

    def refresh_token(self, *args, **kwargs):
        self.auth_token = secrets.token_hex(16)
        super().save(*args, **kwargs)

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
            "image": f"{self.image.url}",
            "header_image": f"{settings.WEB_HOST}{self.header_image.url}"
            if self.header_image
            else None,
            "follower_count": self.follower_count,
            "following_count": self.following_count,
            "verified": self.verified,
            "allow_nsfw": self.allow_nsfw,
        }
