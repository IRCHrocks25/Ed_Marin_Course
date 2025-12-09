from django.contrib import admin
from .models import Course, Module, Lesson, UserProgress, CourseEnrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_type', 'status', 'coach_name', 'is_subscribers_only', 'created_at']
    list_filter = ['course_type', 'status', 'is_subscribers_only', 'is_accredible_certified']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'order']
    list_filter = ['course']
    ordering = ['course', 'order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'module', 'order', 'lesson_type', 'video_duration', 'ai_generation_status']
    list_filter = ['course', 'lesson_type', 'ai_generation_status']
    search_fields = ['title', 'description', 'working_title', 'vimeo_id']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['course', 'order']
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'module', 'title', 'slug', 'order', 'lesson_type')
        }),
        ('Video', {
            'fields': ('video_url', 'vimeo_url', 'vimeo_id', 'vimeo_thumbnail', 'vimeo_duration_seconds', 'video_duration', 'google_drive_url', 'google_drive_id')
        }),
        ('Lesson Creation', {
            'fields': ('working_title', 'rough_notes')
        }),
        ('AI Generated Content', {
            'fields': ('ai_generation_status', 'ai_clean_title', 'ai_short_summary', 'ai_full_description', 'ai_outcomes', 'ai_coach_actions')
        }),
        ('Resources', {
            'fields': ('description', 'workbook_url', 'resources_url')
        }),
    )


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'progress_percentage', 'last_accessed']
    list_filter = ['completed', 'last_accessed']
    search_fields = ['user__username', 'lesson__title']


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'payment_type', 'enrolled_at']
    list_filter = ['payment_type', 'enrolled_at']
    search_fields = ['user__username', 'course__name']
