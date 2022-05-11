from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, JsonResponse
from .models import UrlData
from .forms import ShortenerForm
from django.conf import settings
import json
from random import choice
from string import ascii_letters, digits
from django.views.decorators.csrf import csrf_exempt


def home_view(request):
    template = 'url_fixer/home.html'
    context = dict()
    context['form'] = ShortenerForm()
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        form = ShortenerForm(request.POST)
        if form.is_valid():
            long_url = form.data.get('long_url')
            custom_url = form.data.get('custom_url')
            new_url = mapper(request, long_url, custom_url)
            context['new_url'] = new_url
            context['long_url'] = long_url
            return render(request, template, context)
        context['errors'] = form.errors
        return render(request, template, context)


def mapper(request, long_url, custom_url=None):
    obj = UrlData()
    obj.long_url = long_url
    obj.short_url = create_shortened_url(custom_url)
    obj.save()
    new_url = request.build_absolute_uri('/') + obj.short_url
    return new_url


def redirect_url_view(request, shortened_part):
    try:
        shortener = UrlData.objects.get(short_url=shortened_part)
        shortener.times_followed += 1
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)
    except:
        raise Http404('Sorry this link is broken :(')


def create_shortened_url(custom_url = None):
    if custom_url:
        random_code = custom_url
    else:
        random_code = create_random_code()
        if UrlData.objects.filter(short_url=random_code).exists():
            # Run the function again
            return create_shortened_url()

    return random_code


SIZE = getattr(settings, "MAXIMUM_URL_CHARS", 7)

AVAIABLE_CHARS = ascii_letters + digits


def create_random_code(chars=AVAIABLE_CHARS):
    """
    Creates a random string with the predetermined size
    """
    return "".join(
        [choice(chars) for _ in range(SIZE)]
    )

@csrf_exempt
def all_data(request):
    data = json.loads(request.body)
    short_url = mapper(request, data.get('long_url'))
    return JsonResponse({'short_url': short_url}, status=200)
