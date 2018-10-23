from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'shopApp'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('(?p<category_slug>)/',
         views.product_list,
         name='product_list_by_category'),
    path('(?p<id>\d+)/(?p<slug>)/',
         views.product_detail,
         name='product_detail'),

]

