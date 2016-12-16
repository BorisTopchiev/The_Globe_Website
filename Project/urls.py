from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^materials/$', views.materials_page, name='materials_page'),
    url(r'^registration/$', views.register_page, name='register_page'),
    url(r'^admin/', admin.site.urls),
]
