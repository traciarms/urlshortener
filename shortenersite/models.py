from __future__ import unicode_literals
from django.db import models


class Urls(models.Model):
    """
        Our URLs class - this is where we will store the short_id,
        the original http_url and org_date
    """
    short_id = models.SlugField(max_length=6, primary_key=True)
    http_url = models.URLField(max_length=200)
    org_date = models.DateTimeField(auto_now=True)


def __str__(self):
    return self.http_url
