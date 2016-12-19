from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^blogs/$', views.blogs_page, name='blogs_page'),
    url(r'^add/$', views.add_blog, name='add_page'),
    url(r'^remove/(?P<id>[\w]+)/$', views.remove_post),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^blog_post/(?P<id>[\w]+)/$', views.load_blog, name='blog_post'),
    url(r'^add_comment/(?P<id>[\w]+)/$', views.add_comment),
    url(r'^materials/$', views.materials_page, name='materials_page'),
    url(r'^registration/$', views.register_page, name='register_page'),
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^admin/', admin.site.urls),
]
