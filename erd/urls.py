from django.conf.urls import url
from . import views

app_name='erd'
urlpatterns = [
    url(r'^$', views.PagesView.as_view(), name='pview'),     
]