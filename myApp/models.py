from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class Course(models.Model):
    COURSE_TYPES = [
        ('sprint', 'Sprint'),
        ('speaking', 'Speaking'),
        ('consultancy', 'Consultancy'),
        ('special', 'Special'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('locked', 'Locked'),
        ('coming_soon', 'Coming Soon'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES, default='sprint')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    coach_name = models.CharField(max_length=100, default='Sprint Coach')
    is_subscribers_only = models.BooleanField(default=False)
    is_accredible_certified = models.BooleanField(default=False)
    has_asset_templates = models.BooleanField(default=False)
    exam_unlock_days = models.IntegerField(default=120, help_text="Days after enrollment before exam unlocks")
    special_tag = models.CharField(max_length=100, blank=True, help_text="e.g., 'Black Friday 2025 Special'")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_lesson_count(self):
        return self.lessons.count()
    
    def get_user_progress(self, user):
        if not user.is_authenticated:
            return 0
        completed = UserProgress.objects.filter(user=user, lesson__course=self, completed=True).count()
        total = self.lessons.count()
        if total == 0:
            return 0
        return int((completed / total) * 100)


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    video_url = models.URLField(blank=True)
    video_duration = models.IntegerField(default=0, help_text="Duration in minutes")
    order = models.IntegerField(default=0)
    workbook_url = models.URLField(blank=True)
    resources_url = models.URLField(blank=True)
    lesson_type = models.CharField(max_length=50, default='video', choices=[
        ('video', 'Video'),
        ('live', 'Live Session'),
        ('replay', 'Replay'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Vimeo Integration Fields
    vimeo_url = models.URLField(blank=True, help_text="Full Vimeo URL (e.g., https://vimeo.com/123456789)")
    vimeo_id = models.CharField(max_length=50, blank=True, help_text="Vimeo video ID extracted from URL")
    vimeo_thumbnail = models.URLField(blank=True, help_text="Vimeo thumbnail URL")
    vimeo_duration_seconds = models.IntegerField(default=0, help_text="Duration in seconds from Vimeo")
    
    # Google Drive Integration Fields
    google_drive_url = models.URLField(blank=True, help_text="Google Drive video embed URL")
    google_drive_id = models.CharField(max_length=200, blank=True, help_text="Google Drive file ID")
    
    # Lesson Creation Fields
    working_title = models.CharField(max_length=200, blank=True, help_text="Rough title before AI generation")
    rough_notes = models.TextField(blank=True, help_text="Optional notes or outline for AI")
    
    # AI Generated Content
    ai_generation_status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('generated', 'Generated'),
        ('approved', 'Approved'),
    ])
    ai_clean_title = models.CharField(max_length=200, blank=True, help_text="AI-generated polished title")
    ai_short_summary = models.TextField(blank=True, help_text="AI-generated short summary for lesson list")
    ai_full_description = models.TextField(blank=True, help_text="AI-generated full description for student page")
    ai_outcomes = models.JSONField(default=list, blank=True, help_text="List of outcomes this lesson will produce")
    ai_coach_actions = models.JSONField(default=list, blank=True, help_text="Recommended AI Coach actions for this lesson")
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.course.name} - {self.title}"
    
    def get_vimeo_embed_url(self):
        """Convert Vimeo URL to embed format"""
        if self.vimeo_id:
            return f"https://player.vimeo.com/video/{self.vimeo_id}"
        return ""
    
    def get_formatted_duration(self):
        """Format duration in MM:SS format"""
        if self.vimeo_duration_seconds:
            minutes = self.vimeo_duration_seconds // 60
            seconds = self.vimeo_duration_seconds % 60
            return f"{minutes}:{seconds:02d}"
        elif self.video_duration:
            return f"{self.video_duration}:00"
        return "0:00"
    
    def get_outcomes_list(self):
        """Return outcomes as a list"""
        if isinstance(self.ai_outcomes, list):
            return self.ai_outcomes
        if isinstance(self.ai_outcomes, str):
            try:
                return json.loads(self.ai_outcomes)
            except:
                return []
        return []
    
    def get_coach_actions_list(self):
        """Return coach actions as a list"""
        if isinstance(self.ai_coach_actions, list):
            return self.ai_coach_actions
        if isinstance(self.ai_coach_actions, str):
            try:
                return json.loads(self.ai_coach_actions)
            except:
                return []
        return []


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'lesson']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20, choices=[
        ('full', 'Full Payment'),
        ('installment', 'Installment'),
    ], default='full')
    
    class Meta:
        unique_together = ['user', 'course']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name}"
    
    def days_until_exam(self):
        if self.payment_type == 'full':
            return 0
        days_elapsed = (timezone.now() - self.enrolled_at).days
        return max(0, self.course.exam_unlock_days - days_elapsed)
