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
        

class Badge(models.Model):
    """
    Badge model
    """

    COLOR_CHOICE = (
        ('success', 'Green'),
        ('info', 'Blue'),
        ('link', 'Purple'),
        ('primary', 'Turquoise'),
        ('warning', 'Yellow'),
        ('danger', 'Red'),
        ('dark', 'Black'),
        ('white', 'White'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField()
    color = models.CharField(max_length=50, choices=COLOR_CHOICE)
    special = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Requirments(models.Model):
    """
    Requirments model
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Donation(models.Model):
    """
    Donation model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["-date"]