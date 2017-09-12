from django.conf.urls import url
from django.contrib import admin

from .views import  (
post_list,
post_create,
post_detail,
post_update,
post_delete,
add_comment_to_post,
)


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/comment/$', add_comment_to_post, name='add_comment_to_post'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),  
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name = 'update'),
    url(r'^create/$', post_create),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^$', post_list, name = 'list'),
]


