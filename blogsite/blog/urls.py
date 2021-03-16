from django.urls import path
from . import views

# TIP Creating a urls.py file for each application is the best way to make your applications reusable by other projects.
app_name = 'blog'  # application namespace

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'), #regular function list
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),  # regular function list
    #path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share')
]
