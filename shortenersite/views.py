import random
import string

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from shortenersite.forms import CustomerCreationForm
from shortenersite.models import Urls, UserProfile


def index(request):

    user = request.user
    if user.is_authenticated:

        userprofile = UserProfile.objects.get(user=user)
        urls_set = Urls.objects.filter(user=userprofile)
        return render(request, 'index.html', {'showURL': False,
                                              'showError': False,
                                              'urls_set': urls_set})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def create_user(request):
    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if request.user.is_authenticated():
                user = request.user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
            else:
                user = form.save()
            profile = UserProfile()
            profile.user = user
            profile.user_category = data['user_category']
            profile.save()
            user.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            login(request, user)

            return HttpResponseRedirect(reverse('home'))
    else:
        context = {}
        if request.user and not isinstance(request.user, AnonymousUser):
            user = request.user
            context['username'] = user.username
            context['first_name'] = user.first_name
            context['last_name'] = user.last_name
            context['user_category'] = user.user_category

        form = CustomerCreationForm(initial=context)

    return render(request, 'user_registration.html', {'form': form})


def redirect_original(request, short_id):
    # redirect to the original url, or if not found return 404 error
    url = get_object_or_404(Urls, pk=short_id)
    url.save()

    return HttpResponseRedirect(url.http_url)


@login_required
def urlset(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    urls_set = Urls.objects.filter(user=user_profile)

    return render(request, 'urlset.html', {'urlset': urls_set})


@login_required
def shorten_url(request):
    url = request.POST.get("url", '')
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if not (url == ''):
        short_id = get_short_code()
        b = Urls(http_url=url, short_id=short_id, user=user_profile)
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