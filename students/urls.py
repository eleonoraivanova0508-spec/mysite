from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Главная
    path('', views.student_list, name='student_list'),
    
    # Аутентификация (все здесь)
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    # Студенты
    path('add/', views.add_student, name='add_student'),
    path('detail/<int:id>/', views.student_detail, name='student_detail'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('stats/<int:id>/', views.student_statistics, name='student_stats'),
    
    # Оценки
    path('add-grade/', views.add_grade, name='add_grade'),
    path('overall-stats/', views.overall_stats, name='overall_stats'),
    
    # Профиль
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('password-change/', views.password_change, name='password_change'),
]