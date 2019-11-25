"""stradacore URL Configuration
contains the path for faq and recipes apps, admin,
and ckeditor library uploader
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static

from faq import views

urlpatterns = [
    re_path(r'^$', views.index, name="index"),
    path('faq/', include(('faq.urls', 'faq'), namespace="faq")),
    path('recipes/', include(('recipes.urls', 'recipes'), namespace="recipes")),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
