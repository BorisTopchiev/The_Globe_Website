from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [

    url(r'', views.header),
    url(r'^materials/', views.materials, name='materials_page'),
    url(r'^admin/', admin.site.urls),
]
