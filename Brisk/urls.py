"""
URL configuration for Brisk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blogapp.urls')),
    path('', include('brick.urls')),
    path('', include('pwa.urls')),
    path("accounts/", include('accounts.urls')),
    path("app/", include('briskbrick.urls')),
    # path('manifest.json', TemplateView.as_view(template_name="manifest.json", content_type='application/json')),
    # path('service-worker.js', TemplateView.as_view(template_name="service-worker.js", content_type='application/javascript')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)