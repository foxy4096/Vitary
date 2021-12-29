from django.db import models
from django.contrib.auth.models import User
from apps.vit.models import Vit

class Abuse(models.Model):
    """
    Abuse model
    """
    ABUSE_TYPE = (
        ('1', 'Abuse'),
        ('2', 'Inappropriate'),
        ('3', 'Spam'),
        ('4', 'Bullying'),
        ('5', 'Sexual Content'),
        ('6', 'Other'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    abuse_type = models.CharField(max_length=50, choices=ABUSE_TYPE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    to_vit = models.ForeignKey(Vit, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Abuses'
        ordering = ['-date']
        