from django.conf.urls import url
from django.urls import include, path
from . import api
from rest_framework.authtoken import views

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('login/', views.obtain_auth_token),
    url('init', api.initialize),
    url('move', api.move),
    url('rooms', api.rooms),
    url('say', api.say)
]
