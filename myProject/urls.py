from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myApp import views
from myApp import dashboard_views

urlpatterns = [
    # Public-facing URLs
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('courses/<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    
    # Dashboard URLs (Client-facing, replaces admin)
    path('dashboard/', dashboard_views.dashboard_home, name='dashboard_home'),
    path('dashboard/courses/', dashboard_views.dashboard_courses, name='dashboard_courses'),
    path('dashboard/courses/add/', dashboard_views.dashboard_add_course, name='dashboard_add_course'),
    path('dashboard/courses/<slug:course_slug>/', dashboard_views.dashboard_course_detail, name='dashboard_course_detail'),
    path('dashboard/courses/<slug:course_slug>/lessons/', dashboard_views.dashboard_course_lessons, name='dashboard_course_lessons'),
    path('dashboard/lessons/', dashboard_views.dashboard_lessons, name='dashboard_lessons'),
    path('dashboard/lessons/add/', dashboard_views.dashboard_add_lesson, name='dashboard_add_lesson'),
    path('dashboard/lessons/<int:lesson_id>/edit/', dashboard_views.dashboard_edit_lesson, name='dashboard_edit_lesson'),
    
    # Creator/Lesson Upload Flow (kept for lesson creation)
    path('creator/courses/<slug:course_slug>/add-lesson/', views.add_lesson, name='add_lesson'),
    path('creator/courses/<slug:course_slug>/lessons/<int:lesson_id>/generate/', views.generate_lesson_ai, name='generate_lesson_ai'),
    path('creator/verify-vimeo/', views.verify_vimeo_url, name='verify_vimeo_url'),
    
    # Admin (optional - can be removed if not needed)
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
