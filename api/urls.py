from django.urls import include, path
from django.conf.urls import url


urlpatterns = [
    path('', include('rest_auth.urls')),
]
