from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('create_task/', views.create_task, name='create_task'),
    path('edit_task/<uuid:uuid>/', views.edit_task, name='edit_task'),
    path('delete_task/<uuid:uuid>/', views.delete_task, name='delete_task'),
    path('finish_task/<uuid:uuid>/', views.finish_task, name='finish_task'),
    path('revise_task/<uuid:uuid>/', views.revise_task, name='revise_task'),
    path('exam/', views.exam, name="exam"),
]
