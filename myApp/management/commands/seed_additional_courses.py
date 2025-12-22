from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myApp.models import Course, Module, Lesson
import json


class Command(BaseCommand):
    help = 'Seed the database with 2 additional sample courses and lessons'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed additional courses...'))
        
        # Google Drive video URLs for lessons (using placeholder format - replace with actual URLs)
        GOOGLE_DRIVE_VIDEOS = [
            "https://drive.google.com/file/d/1vjh0c7ReJn4YjFsgcBCSJKW4xhJg3JOp/preview",
            "https://drive.google.com/file/d/15LLxGCE3gzMPpo4j7K5yyzaQmt9sTKHd/preview",
            "https://drive.google.com/file/d/1c4DpGIwhRJo5ZrasVnRM4JJZdFLupvaw/preview",
            "https://drive.google.com/file/d/1ItvLVPWsmdb9yoKDINcyIyOoa1IMCtcT/preview",
            "https://drive.google.com/file/d/1z7NwNXfgEtZdLouj8b2wZu-YHHpfl2Nm/preview",
            "https://drive.google.com/file/d/1Wv06ZSdCzzb4TwdydHM_UF_I9bdhNsk3/preview",
        ]
        
        # Course 1: AI-Powered Sales Mastery
        course1, created1 = Course.objects.get_or_create(
            slug='ai-powered-sales-mastery',
            defaults={
                'name': 'AI-Powered Sales Mastery',
                'course_type': 'sprint',
                'status': 'active',
                'description': 'Transform your sales process with AI. Learn how to leverage artificial intelligence to close more deals, automate follow-ups, and scale your sales operations. This comprehensive course covers everything from AI-powered CRM systems to automated email sequences and intelligent lead scoring.',
                'short_description': 'Master AI tools and strategies to revolutionize your sales process and close more deals.',
                'coach_name': 'Sales AI Coach',
                'is_subscribers_only': False,
                'is_accredible_certified': True,
                'has_asset_templates': True,
                'exam_unlock_days': 90,
                'visibility': 'public',
                'enrollment_method': 'open',
                'access_duration_type': 'lifetime',
            }
        )
        
        if created1:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course1.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Course {course1.name} already exists'))
            course1.lessons.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing lessons'))
        
        # Create Module for Course 1
        module1, _ = Module.objects.get_or_create(
            course=course1,
            name='AI Sales Fundamentals',
            defaults={'order': 0, 'description': 'Core AI sales strategies and implementation'}
        )
        
        # Lessons for Course 1
        course1_lessons = [
            {
                'title': 'Introduction to AI in Sales',
                'slug': 'introduction-ai-sales',
                'order': 1,
                'description': 'Discover how AI is transforming the sales landscape and learn the fundamentals of integrating AI into your sales process.',
                'vimeo_duration_seconds': 1800,  # 30 minutes
                'video_duration': 30,
            },
            {
                'title': 'AI-Powered Lead Generation',
                'slug': 'ai-lead-generation',
                'order': 2,
                'description': 'Learn how to use AI tools to identify, qualify, and prioritize leads automatically, saving hours of manual work.',
                'vimeo_duration_seconds': 2400,  # 40 minutes
                'video_duration': 40,
            },
            {
                'title': 'Automated Email Sequences',
                'slug': 'automated-email-sequences',
                'order': 3,
                'description': 'Master the art of creating AI-powered email sequences that nurture leads and convert prospects into customers.',
                'vimeo_duration_seconds': 2100,  # 35 minutes
                'video_duration': 35,
            },
            {
                'title': 'AI CRM Integration',
                'slug': 'ai-crm-integration',
                'order': 4,
                'description': 'Integrate AI capabilities into your CRM system to automate data entry, predict deal outcomes, and optimize your sales pipeline.',
                'vimeo_duration_seconds': 2700,  # 45 minutes
                'video_duration': 45,
            },
            {
                'title': 'Sales Forecasting with AI',
                'slug': 'sales-forecasting-ai',
                'order': 5,
                'description': 'Use AI to predict sales outcomes, identify at-risk deals, and make data-driven decisions about your sales strategy.',
                'vimeo_duration_seconds': 2400,  # 40 minutes
                'video_duration': 40,
            },
            {
                'title': 'Closing Deals with AI Assistance',
                'slug': 'closing-deals-ai',
                'order': 6,
                'description': 'Learn advanced techniques for using AI to identify the best closing strategies and personalize your approach for each prospect.',
                'vimeo_duration_seconds': 2100,  # 35 minutes
                'video_duration': 35,
            },
        ]
        
        # Create lessons for Course 1
        for index, lesson_data in enumerate(course1_lessons):
            google_drive_url = GOOGLE_DRIVE_VIDEOS[index] if index < len(GOOGLE_DRIVE_VIDEOS) else ""
            
            lesson, created = Lesson.objects.get_or_create(
                course=course1,
                slug=lesson_data['slug'],
                defaults={
                    'module': module1,
                    'title': lesson_data['title'],
                    'order': lesson_data['order'],
                    'description': lesson_data['description'],
                    'google_drive_url': google_drive_url,
                    'google_drive_id': google_drive_url.split('/d/')[1].split('/')[0] if '/d/' in google_drive_url else '',
                    'vimeo_duration_seconds': lesson_data['vimeo_duration_seconds'],
                    'video_duration': lesson_data['video_duration'],
                    'ai_generation_status': 'approved',
                    'ai_clean_title': lesson_data['title'],
                    'ai_short_summary': lesson_data['description'],
                    'ai_full_description': f'''{lesson_data['description']}

This lesson is part of the AI-Powered Sales Mastery program, designed to help you leverage artificial intelligence to transform your sales process. You'll learn practical strategies, implement key frameworks, and walk away with tangible tools that increase your sales efficiency and results.

By the end of this lesson, you'll have actionable insights and a clear implementation plan.''',
                    'ai_outcomes': [
                        'Clear understanding of AI applications in sales',
                        'Practical frameworks for immediate implementation',
                        'Step-by-step action plan',
                        'Tools and resources checklist'
                    ],
                    'ai_coach_actions': [
                        'Summarize key takeaways in 5 bullets',
                        'Create a 3-step implementation plan',
                        'Generate 3 follow-up email templates',
                        'Create a comprehension quiz'
                    ],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {lesson.title}'))
            else:
                lesson.google_drive_url = google_drive_url
                lesson.google_drive_id = google_drive_url.split('/d/')[1].split('/')[0] if '/d/' in google_drive_url else ''
                lesson.vimeo_duration_seconds = lesson_data['vimeo_duration_seconds']
                lesson.video_duration = lesson_data['video_duration']
                lesson.description = lesson_data['description']
                lesson.order = lesson_data['order']
                lesson.save()
                self.stdout.write(self.style.WARNING(f'  ↻ Updated lesson: {lesson.title}'))
        
        # Course 2: Content Creation with AI
        course2, created2 = Course.objects.get_or_create(
            slug='content-creation-with-ai',
            defaults={
                'name': 'Content Creation with AI',
                'course_type': 'special',
                'status': 'active',
                'description': 'Create high-quality content at scale using AI. Learn how to use AI tools to write blog posts, create social media content, produce videos, and develop comprehensive content strategies. Perfect for marketers, content creators, and business owners who want to scale their content production.',
                'short_description': 'Master AI-powered content creation tools to produce engaging content faster and more efficiently.',
                'coach_name': 'Content AI Coach',
                'is_subscribers_only': False,
                'is_accredible_certified': True,
                'has_asset_templates': True,
                'exam_unlock_days': 60,
                'visibility': 'public',
                'enrollment_method': 'open',
                'access_duration_type': 'lifetime',
            }
        )
        
        if created2:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course2.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Course {course2.name} already exists'))
            course2.lessons.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing lessons'))
        
        # Create Module for Course 2
        module2, _ = Module.objects.get_or_create(
            course=course2,
            name='AI Content Mastery',
            defaults={'order': 0, 'description': 'Complete guide to AI-powered content creation'}
        )
        
        # Lessons for Course 2
        course2_lessons = [
            {
                'title': 'AI Writing Tools Mastery',
                'slug': 'ai-writing-tools-mastery',
                'order': 1,
                'description': 'Explore the best AI writing tools and learn how to craft compelling blog posts, articles, and long-form content using AI assistance.',
                'vimeo_duration_seconds': 2400,  # 40 minutes
                'video_duration': 40,
            },
            {
                'title': 'Social Media Content at Scale',
                'slug': 'social-media-content-scale',
                'order': 2,
                'description': 'Create engaging social media posts, captions, and content calendars using AI to maintain consistent, high-quality output.',
                'vimeo_duration_seconds': 2100,  # 35 minutes
                'video_duration': 35,
            },
            {
                'title': 'Video Script Writing with AI',
                'slug': 'video-script-writing-ai',
                'order': 3,
                'description': 'Learn how to use AI to write compelling video scripts that engage viewers and drive action, from YouTube videos to marketing content.',
                'vimeo_duration_seconds': 2700,  # 45 minutes
                'video_duration': 45,
            },
            {
                'title': 'Email Marketing Content',
                'slug': 'email-marketing-content',
                'order': 4,
                'description': 'Master AI-powered email content creation, from subject lines to full email sequences that convert subscribers into customers.',
                'vimeo_duration_seconds': 1800,  # 30 minutes
                'video_duration': 30,
            },
            {
                'title': 'Content Strategy & Planning',
                'slug': 'content-strategy-planning',
                'order': 5,
                'description': 'Develop comprehensive content strategies using AI to identify topics, plan content calendars, and optimize for your audience.',
                'vimeo_duration_seconds': 2400,  # 40 minutes
                'video_duration': 40,
            },
            {
                'title': 'SEO-Optimized Content Creation',
                'slug': 'seo-optimized-content',
                'order': 6,
                'description': 'Create SEO-friendly content using AI tools that rank well in search engines while maintaining high quality and readability.',
                'vimeo_duration_seconds': 2100,  # 35 minutes
                'video_duration': 35,
            },
        ]
        
        # Create lessons for Course 2
        for index, lesson_data in enumerate(course2_lessons):
            google_drive_url = GOOGLE_DRIVE_VIDEOS[index] if index < len(GOOGLE_DRIVE_VIDEOS) else ""
            
            lesson, created = Lesson.objects.get_or_create(
                course=course2,
                slug=lesson_data['slug'],
                defaults={
                    'module': module2,
                    'title': lesson_data['title'],
                    'order': lesson_data['order'],
                    'description': lesson_data['description'],
                    'google_drive_url': google_drive_url,
                    'google_drive_id': google_drive_url.split('/d/')[1].split('/')[0] if '/d/' in google_drive_url else '',
                    'vimeo_duration_seconds': lesson_data['vimeo_duration_seconds'],
                    'video_duration': lesson_data['video_duration'],
                    'ai_generation_status': 'approved',
                    'ai_clean_title': lesson_data['title'],
                    'ai_short_summary': lesson_data['description'],
                    'ai_full_description': f'''{lesson_data['description']}

This lesson is part of the Content Creation with AI program, designed to help you leverage artificial intelligence to create high-quality content at scale. You'll learn practical strategies, master key tools, and walk away with templates and frameworks you can use immediately.

By the end of this lesson, you'll have actionable content creation strategies and ready-to-use templates.''',
                    'ai_outcomes': [
                        'Mastery of AI content creation tools',
                        'Ready-to-use content templates',
                        'Clear content strategy framework',
                        'Implementation checklist'
                    ],
                    'ai_coach_actions': [
                        'Summarize key content creation principles',
                        'Generate 5 content ideas based on this lesson',
                        'Create a content template',
                        'Develop a content calendar outline'
                    ],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {lesson.title}'))
            else:
                lesson.google_drive_url = google_drive_url
                lesson.google_drive_id = google_drive_url.split('/d/')[1].split('/')[0] if '/d/' in google_drive_url else ''
                lesson.vimeo_duration_seconds = lesson_data['vimeo_duration_seconds']
                lesson.video_duration = lesson_data['video_duration']
                lesson.description = lesson_data['description']
                lesson.order = lesson_data['order']
                lesson.save()
                self.stdout.write(self.style.WARNING(f'  ↻ Updated lesson: {lesson.title}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Additional courses seeding completed!'))
        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary:'))
        self.stdout.write(self.style.SUCCESS(f'   - Course 1: {course1.name} ({Lesson.objects.filter(course=course1).count()} lessons)'))
        self.stdout.write(self.style.SUCCESS(f'   - Course 2: {course2.name} ({Lesson.objects.filter(course=course2).count()} lessons)'))
        self.stdout.write(self.style.SUCCESS(f'\n🔗 Access your courses:'))
        self.stdout.write(self.style.SUCCESS(f'   Course 1: http://127.0.0.1:8000/courses/{course1.slug}/'))
        self.stdout.write(self.style.SUCCESS(f'   Course 2: http://127.0.0.1:8000/courses/{course2.slug}/'))
        self.stdout.write(self.style.SUCCESS(f'   All Courses: http://127.0.0.1:8000/courses/'))

