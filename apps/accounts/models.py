from django.db import models

from django.utils.safestring import mark_safe

from django.contrib.auth.models import User
from apps.core.models import Badge



class Profile(models.Model):
    """
    Extending the base user model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/',
                              default='/uploads/default.jpg', verbose_name='Profile Image')
    follows = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False)
    follower_count = models.IntegerField(default=0, editable=False)
    following_count = models.IntegerField(default=0, editable=False)
    email_notif = models.BooleanField(
        default=True, verbose_name="Get Email Notifications")
    verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True, null=True, default="")
    header_image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    badges = models.ManyToManyField(Badge)

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
        return reverse('profile_view', kwargs={'username': self.user.username})

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
        return mark_safe(f'<img src="{self.get_image_url()}" height=50 / style="border-radius: 10%">')

    def to_json(self):
        """
        Returns a json representation of the model
        """
        return {
            'id': self.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'bio': self.bio,
            'image': self.image.url,
            'header_image': self.header_image.url,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'verified': self.verified,
        }

class Group(models.Model):
    """
    Group model
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)
    image = models.ImageField(upload_to='uploads/',
                                default='/uploads/default.jpg', verbose_name='Group Image')
    members = models.ManyToManyField(User, related_name='user_groups')
    admin = models.ManyToManyField(User)
    date = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False, verbose_name="Public Group")

    def __str__(self):
        """
        String representation of the model
        """
        return self.name

    def get_absolute_url(self): 
        """
        Returns the absolute url to the group
        """
        from django.urls import reverse
        return reverse('group_view', kwargs={'slug': self.slug})

    def to_json(self):
        """
        Returns a json representation of the model
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'image': self.image.url,
            'members': [member.to_json() for member in self.members.all()],
            'admin': self.admin.all(),
            'date': self.date,
            'is_public': self.is_public,
        }

class GroupInvitation(models.Model):
    """
    Group invitation model
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the model
        """
        return self.user.username + " to " + self.group.name

    def to_json(self):
        """
        Returns a json representation of the model
        """
        return {
            'id': self.id,
            'group': self.group.to_json(),
            'user': self.user.profile.to_json(),
            'date': self.date,
            'is_accepted': self.is_accepted,
        }

    def accept(self):
        """
        Accepts the invitation
        """
        self.is_accepted = True
        self.save()
        self.group.members.add(self.user)
        self.group.save()
        
