from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='Student/generic_form.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('students/', views.student_list, name='student_list'),
    path('student/add/', views.student_create, name='student_create'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/<int:pk>/edit/', views.student_update, name='student_update'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    path('achievement/add/', views.achievement_create, name='achievement_create'),
    path('achievement/<int:pk>/edit/', views.achievement_update, name='achievement_update'),
    path('achievement/<int:pk>/delete/', views.achievement_delete, name='achievement_delete'),
    path('achievement/<int:pk>/status/<str:status>/', views.update_achievement_status, name='update_achievement_status'),
]