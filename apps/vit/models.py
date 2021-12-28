from django.db import models

from django.contrib.auth.models import User


class Vit(models.Model):
    """
    Vit model
    """
    body = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vits")
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/images/', blank=True,
                              null=True, help_text="You can upload upto one image per Vit")
    video = models.FileField(upload_to='uploads/videos/', blank=True,
                             null=True, help_text="You can upload upto one video per Vit")
    likes = models.ManyToManyField(User, related_name="liked_vits")
    like_count = models.IntegerField(default=0)
    plustag = models.ManyToManyField('Plustag', blank=True)
    to_reply_vits = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="To Reply Vit", related_name='reply')


    def save(self, *args, **kwargs):
        self.body = self.body.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vit No.{self.pk} by {self.user.username.title()}"

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.video.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('vit_detail', kwargs={'pk': self.pk})

    def latest_vits():
        return Vit.objects.all().order_by('-like_count', '-date')[:5]


class Plustag(models.Model):
    """
    Hashtag model
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
