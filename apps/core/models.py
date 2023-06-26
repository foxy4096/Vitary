from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from django.contrib import admin


class Report(models.Model):
    """
    Report model
    """

    REPORT_TYPE = (
        ("ABUSE", "Abuse"),
        ("INAPPROPRIATE", "Inappropriate"),
        ("SPAM", "Spam"),
        ("BULLYING", "Bullying"),
        ("SEXUAL_CONTENT", "Sexual Content"),
        ("OTHER", "Other"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Created By")
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE)
    description = models.TextField(help_text="You can give us some more details.")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    url = models.URLField("URL to be reported")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Reports"
        ordering = ["-date"]


class Badge(models.Model):
    """
    Badge model
    """

    COLOR_CHOICE = (
        ("success", "Green"),
        ("info", "Blue"),
        ("link", "Purple"),
        ("primary", "Turquoise"),
        ("warning", "Yellow"),
        ("danger", "Red"),
        ("dark", "Black"),
        ("white", "White"),
    )

    name = models.CharField(max_length=50)
    description = models.TextField()
    color = models.CharField(max_length=50, choices=COLOR_CHOICE)
    special = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Document(models.Model):
    FILE_TYPE = (
        ("IMAGE", "image"),
        ("VIDEO", "video"),
        ("AUDIO", "audio"),
        ("OTHER", "other"),
    )
    file_type = models.CharField(max_length=10, choices=FILE_TYPE, default="IMAGE")
    file = models.FileField(upload_to="files/")

    @admin.display
    def file_url(self):
        return settings.WEB_HOST + self.file.url
    
    def __str__(self):
        return self.file.name
