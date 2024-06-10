from django.contrib.auth import get_user_model
from django.db import models
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .utils import get_gravatar
from apps.core.models import Badge



User = get_user_model()


def get_sentinel_user():
    return User.objects.get_or_create(username="ghost", is_active=False)[0]


class UserProfile(models.Model):
    """
    Extending the base user model
    """

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
    header_image = ResizedImageField(
        upload_to="headers/",
        size=[1600, 400],
        crop=["middle", "center"],
        blank=True,
        null=True,
    )
    avatar_image = ResizedImageField(
        size=[600, 600],
        crop=["middle", "center"],
        upload_to="avatars/",
        default="/defaults/avatar.jpg",
        verbose_name="UserProfile Image",
    )
    use_gravatar = models.BooleanField(default=False)
    badges = models.ManyToManyField(Badge, blank=True)
    date_of_birth = models.DateField(
        blank=True, null=True, help_text="It help to know when is your birthday"
    )
    allow_nsfw = models.BooleanField("Allow NSFW Content", default=False)

    def __str__(self):
        """
        String representation of the model
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Returns the absolute url to the userprofile
        """
        from django.urls import reverse

        return reverse("user_detail", kwargs={"username": self.user.username})

    def get_4_followers(self):
        """
        Returns the 4 most recent followers
        """
        return self.follows.all().order_by("-id")[:4]

    def get_4_following(self):
        """
        Returns the 4 most recent follows
        """
        return self.followed_by.all().order_by("-id")[:4]

    def avatar(self):
        return get_gravatar(self.user.email) if self.use_gravatar else f"{settings.WEB_HOST}{self.avatar_image.url}"
