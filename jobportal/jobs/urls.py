from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('employer/', views.employer_dashboard, name='employer_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('view-applicants/<int:job_id>/', views.view_applicants, name='view_applicants'),
    
    path('', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applicant/', views.applicant_dashboard, name='applicant_dashboard'),
]
