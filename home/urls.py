from django.urls import path
from .views import scan_page, progress, result, browse_result, fix_code
from django.contrib.auth.views import (
    LoginView,
)

urlpatterns = [
    path('', scan_page, name='home'),
    path('scan/', scan_page, name='scan'),
    path('progress/<str:task_id>/', progress, name='progress'),
    path('browse_result/', browse_result, name='browse_result'),
    path('result/<str:website>', result, name='result'),
    path('fix_code', fix_code, name='fix_code'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]