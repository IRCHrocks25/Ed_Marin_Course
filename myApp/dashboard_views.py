from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q
import json
import re
import requests
from .models import Course, Lesson, Module, UserProgress, CourseEnrollment


@staff_member_required
def dashboard_home(request):
    """Main dashboard overview"""
    total_courses = Course.objects.count()
    total_lessons = Lesson.objects.count()
    approved_lessons = Lesson.objects.filter(ai_generation_status='approved').count()
    pending_lessons = Lesson.objects.filter(ai_generation_status='pending').count()
    recent_lessons = Lesson.objects.select_related('course').order_by('-created_at')[:10]
    courses = Course.objects.annotate(lesson_count=Count('lessons')).order_by('-created_at')
    
    return render(request, 'dashboard/home.html', {
        'total_courses': total_courses,
        'total_lessons': total_lessons,
        'approved_lessons': approved_lessons,
        'pending_lessons': pending_lessons,
        'recent_lessons': recent_lessons,
        'courses': courses,
    })


@staff_member_required
def dashboard_courses(request):
    """List all courses"""
    courses = Course.objects.annotate(lesson_count=Count('lessons')).order_by('-created_at')
    return render(request, 'dashboard/courses.html', {
        'courses': courses,
    })


@staff_member_required
def dashboard_course_detail(request, course_slug):
    """Edit course details"""
    course = get_object_or_404(Course, slug=course_slug)
    
    if request.method == 'POST':
        course.name = request.POST.get('name', course.name)
        course.short_description = request.POST.get('short_description', course.short_description)
        course.description = request.POST.get('description', course.description)
        course.status = request.POST.get('status', course.status)
        course.course_type = request.POST.get('course_type', course.course_type)
        course.coach_name = request.POST.get('coach_name', course.coach_name)
        course.save()
        return redirect('dashboard_course_detail', course_slug=course.slug)
    
    return render(request, 'dashboard/course_detail.html', {
        'course': course,
    })


@staff_member_required
def dashboard_course_lessons(request, course_slug):
    """View all lessons for a course"""
    course = get_object_or_404(Course, slug=course_slug)
    lessons = course.lessons.all()
    modules = course.modules.all()
    
    return render(request, 'dashboard/course_lessons.html', {
        'course': course,
        'lessons': lessons,
        'modules': modules,
    })


@staff_member_required
def dashboard_add_course(request):
    """Add new course"""
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = generate_slug(name)
        short_description = request.POST.get('short_description', '')
        description = request.POST.get('description', '')
        course_type = request.POST.get('course_type', 'sprint')
        status = request.POST.get('status', 'active')
        coach_name = request.POST.get('coach_name', 'Sprint Coach')
        
        course = Course.objects.create(
            name=name,
            slug=slug,
            short_description=short_description,
            description=description,
            course_type=course_type,
            status=status,
            coach_name=coach_name,
        )
        return redirect('dashboard_course_detail', course_slug=course.slug)
    
    return render(request, 'dashboard/add_course.html')


@staff_member_required
def dashboard_lessons(request):
    """List all lessons across all courses"""
    lessons = Lesson.objects.select_related('course', 'module').order_by('-created_at')
    
    # Filtering
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        lessons = lessons.filter(ai_generation_status=status_filter)
    
    course_filter = request.GET.get('course', '')
    if course_filter:
        lessons = lessons.filter(course_id=course_filter)
    
    courses = Course.objects.all()
    
    return render(request, 'dashboard/lessons.html', {
        'lessons': lessons,
        'courses': courses,
        'status_filter': status_filter,
        'course_filter': course_filter,
    })


@staff_member_required
def dashboard_add_lesson(request):
    """Add new lesson - redirects to creator flow"""
    course_id = request.GET.get('course')
    if course_id:
        course = get_object_or_404(Course, id=course_id)
        return redirect('add_lesson', course_slug=course.slug)
    
    courses = Course.objects.all()
    return render(request, 'dashboard/select_course.html', {
        'courses': courses,
    })


@staff_member_required
def dashboard_edit_lesson(request, lesson_id):
    """Edit lesson - redirects to AI generation page"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return redirect('generate_lesson_ai', course_slug=lesson.course.slug, lesson_id=lesson.id)


# Helper functions (imported from views.py or defined here)
def generate_slug(text):
    """Generate URL-friendly slug from text"""
    import unicodedata
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

