from django.db import models

from django.utils.safestring import mark_safe

from django.contrib.auth.models import User
from apps.core.models import Badge

from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()

class Profile(models.Model):
    """
    Extending the base user model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/',
                              default='/uploads/default.jpg', storage=gd_storage)
    follows = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False)
    follower_count = models.IntegerField(default=0, editable=False)
    following_count = models.IntegerField(default=0, editable=False)
    email_notif = models.BooleanField(
        default=True, verbose_name="Get Email Notifications")
    verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True, null=True, default="")
    header_image = models.ImageField(upload_to='uploads/', blank=True, null=True, storage=gd_storage)
    badges = models.ManyToManyField(Badge)

    def __str__(self):
        return self.user.username

    def get_image_url(self):
        if self.image.url:
            return self.image.url
        else:
            return 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('profile_view', kwargs={'username': self.user.username})

    def get_4_followers(self):
        return self.follows.all()[:4]

    def get_4_following(self):
        return self.followed_by.all()[:4]

    def profile_image(self):
        return mark_safe(f'<img src="{self.get_image_url()}" height=50 / style="border-radius: 50%">')
