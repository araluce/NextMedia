"""NextMedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from NextMedia import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index/', views.index, name='index'),
	url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^registro/', views.registro, name='registro'),
    url(r'^editar/', views.editar, name='editar'),
    url(r'^info$', views.info, name='info'),
    url(r'^subir/', views.subir, name='subir'),
    url(r'^directorio$', views.directorio, name='directorio'),
    url(r'^like_video/$', views.like_video, name='like_video'),
    url(r'^dislike_video/$', views.dislike_video, name='dislike_video'),
    url(r'^visitas_usuarios/$', views.visitas_usuarios, name='visitas_usuarios'),
    url(r'^likes_videos/$', views.likes_videos, name='likes_videos'),
    url(r'^dislikes_videos/$', views.dislikes_videos, name='dislikes_videos'),
    url(r'^estadisticas/', views.estadisticas, name='estadisticas'),
    url(r'^admin/', admin.site.urls),
]
