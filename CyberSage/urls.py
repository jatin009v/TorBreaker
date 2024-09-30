"""
URL configuration for CyberSage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        return HttpResponseRedirect(reverse_lazy('user_verifcation'))

# Create an instance of CustomAdminSite
custom_admin_site = CustomAdminSite(name='admin')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', custom_admin_site.urls),
    path('', include ('home.urls')),
    path('celery-progress/', include('celery_progress.urls')),
]

admin.site.site_header = "CyberSage - Admin"
admin.site.site_title = "CyberSage Admin Portal"
admin.site.index_title = "Welcome to Admin Portal"