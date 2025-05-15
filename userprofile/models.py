from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        # agar user delete hua to uske sarey blogs delete ho jayenge.
        on_delete=models.CASCADE,
    )
    liked_blog_ids = models.TextField(default='[]')
    # liked_blog_ids = models.JSONField(default=dict)
    # liked_blog_ids = models.JSONField(default=list)

    bookmark = models.TextField(default='[]')

    def __str__(self):
        return self.user.username
