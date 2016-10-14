import json
import random
import string

from django.conf import settings
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from shortenersite.models import Urls


def index(request):

    return render(request, 'index.html', {'showURL': False,
                                          'showError': False})


def redirect_original(request, short_id):
    # redirect to the original url, or if not found return 404 error
    url = get_object_or_404(Urls, pk=short_id)
    url.save()

    return HttpResponseRedirect(url.http_url)


def shorten_url(request):
    url = request.POST.get("url", '')

    if not (url == ''):
        short_id = get_short_code()
        b = Urls(http_url=url, short_id=short_id)
        b.save()

        response_data = {}
        response_data['url'] = settings.SITE_URL + "/" + short_id

        return render(request, 'index.html',
                      {'showURL': True,
                       'showError': False,
                       'shortenedURL': response_data.get('url')})

    return render(request, 'index.html', {'showError': True,
                                          'showURL': False,
                                          'errorText': 'Please enter the URL to shorten'})


def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase

    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            Urls.objects.get(pk=short_id)
        except:
            return short_id