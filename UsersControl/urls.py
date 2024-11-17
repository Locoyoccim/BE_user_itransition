from django.urls import path
from . import views

urlpatterns =[
    path('users/', views.get_users),
    path('user/<int:id>/', views.user_path)
]