#inventory/urls.py

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list', views.inventory_list, name='inventory_list'),
    url(r'^new', views.new_item, name='new_item'),
]