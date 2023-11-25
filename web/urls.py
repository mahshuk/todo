from django.urls import path
from django.contrib.auth.views import LoginView
from .views import MarkSheetListView

app_name = "web"

urlpatterns = [
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('marksheet/', MarkSheetListView.as_view(), name='marksheet'),
    # Add other URLs as needed
]
