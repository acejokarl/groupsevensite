from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('sidebar/', views.sidebar_view, name='Sidebar'),
    
    path('gender/list/', views.genders_list),
    path('gender/add/', views.add_gender),
    path('gender/edit/<int:genderId>/', views.edit_gender),
    path('gender/delete/<int:genderId>/', views.delete_gender),

    path('user/list/', views.user_list, name='user_list'), 
    path('user/add/', views.add_user),
    path('user/edit/<int:userId>/', views.edit_user),
    path('user/delete/<int:userId>/', views.delete_user),
]
