from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
        This is the customer model for storing the customer profile info
    """
    QUALIFIED = 'Q'
    NONQUALIFIED = 'N'
    USER_CHOICES = (
        (QUALIFIED, 'Qualified User'),
        (NONQUALIFIED, 'Non-Qualified User')
    )
    user = models.OneToOneField(User)
    user_category = models.CharField(max_length=1, choices=USER_CHOICES,
                                     verbose_name='Qualified User')


class Urls(models.Model):
    """
        Our URLs class - this is where we will store the short_id,
        the original http_url and org_date
    """
    short_id = models.SlugField(max_length=6, primary_key=True)
    http_url = models.URLField(max_length=200)
    org_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, null=True)

    def __str__(self):
        return self.http_url


