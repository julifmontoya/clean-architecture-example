from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve 
from django.urls import re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include("modules.catalog.presentation.urls")),
    path("v1/", include("modules.inventory.presentation.urls")),
    path("v1/", include("modules.featured_tours.presentation.urls")),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]