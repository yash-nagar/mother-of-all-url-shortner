from django.conf.urls import url
from django.contrib import admin
from url_fixer.views import home_view, redirect_url_view, all_data

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^$", home_view, name='home'),
    url(r'^api/data/', all_data),
    url(r'^([a-zA-Z0-9]+)', redirect_url_view, name='redirect'),
]
