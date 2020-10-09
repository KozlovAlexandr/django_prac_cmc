"""paste_shortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import os

PASTE_PREFIX = ""
SHRT_PREFIX = ""

if os.name != 'nt':
    PASTE_PREFIX = '/paste'
    SHRT_PREFIX = '/shrt'

urlpatterns = [
    path(PASTE_PREFIX + 'admin/', admin.site.urls),
    path(PASTE_PREFIX + 'paste/', include('paste.urls')),
    path(SHRT_PREFIX + 'shrt/', include('shortener.urls')),
    path(PASTE_PREFIX + '', include('common.urls')),
] + static(PASTE_PREFIX + settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
