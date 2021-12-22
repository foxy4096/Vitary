from django.db import models

from django.utils.safestring import mark_safe

from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extending the base user model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/',
                              default='/img/default.jpg')
    follows = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False)
    email_notif = models.BooleanField(
        default=True, verbose_name="Get Email Notifications")
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        self.avatar.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('profile_view', kwargs={'username': self.user.username})

    def get_4_followers(self):
        return self.follows.all()[:4]

    def get_4_following(self):
        return self.followed_by.all()[:4]

    def profile_image(self):
        return mark_safe(f'<img src="{self.image.url}" height=50 />')
