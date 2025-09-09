from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('project/<uuid:project_id>/', views.project_detail, name='project_detail'),
    path('skills/', views.skills, name='skills'),
    path('contact/', views.contact, name='contact'),
    
    # API endpoints
    path('api/skills/', views.api_skills, name='api_skills'),
    path('api/projects/', views.api_projects, name='api_projects'),
]