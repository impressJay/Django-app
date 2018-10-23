from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('tag/(?p<tag_slug>[-\w]+[\u4e00-\u9fa5])/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('(?p<year>\d{4})/(?p<month>\d{2})/(?p<day>\d{2})/(?p<post>[-\w]+)/',
         views.post_detail,
         name='post_detail'),
    path('(?p<post_id>\d+)/share/', views.post_share,
         name='post_share'),

]