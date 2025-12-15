
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myApp.models import Course, Module, Lesson
import json


class Command(BaseCommand):
    help = 'Seed the database with sample courses and lessons'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed database...'))
        
        # Create or get admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        
        # Google Drive video URLs (embed format) - 12 unique videos for 12 lessons
        GOOGLE_DRIVE_VIDEOS = [
            "https://drive.google.com/file/d/1vjh0c7ReJn4YjFsgcBCSJKW4xhJg3JOp/preview",  # 1st
            "https://drive.google.com/file/d/15LLxGCE3gzMPpo4j7K5yyzaQmt9sTKHd/preview",  # 2nd
            "https://drive.google.com/file/d/1c4DpGIwhRJo5ZrasVnRM4JJZdFLupvaw/preview",  # 3rd
            "https://drive.google.com/file/d/1ItvLVPWsmdb9yoKDINcyIyOoa1IMCtcT/preview",  # 4th (kept, 5th was duplicate)
            "https://drive.google.com/file/d/1z7NwNXfgEtZdLouj8b2wZu-YHHpfl2Nm/preview",  # 5th (was 6th)
            "https://drive.google.com/file/d/1Wv06ZSdCzzb4TwdydHM_UF_I9bdhNsk3/preview",  # 6th (was 7th)
            "https://drive.google.com/file/d/1paEt7fjQAc3MD_82JWA-oOZzJ7_MD82f/preview",  # 7th (was 8th)
            "https://drive.google.com/file/d/1geHiehW3AOx80b2p2_TGSXLAjjcWBryX/preview",  # 8th (was 9th)
            "https://drive.google.com/file/d/1-bCMwhgBrAW80en5lWIYURBh-XOWWBrn/preview",  # 9th (was 10th)
            "https://drive.google.com/file/d/1tyNbO0k1QgL5thBxAndEWr8fLHyAMNjZ/preview",  # 10th (was 11th)
            "https://drive.google.com/file/d/1sxRMfRi70UmEetf4bbSELMehXM8C38K4/preview",  # 11th (was 12th)
            "https://drive.google.com/file/d/1rvZR8uldp-dTgwsx7rbPkKmYFeUq2N5x/preview",  # 12th (was 13th)
        ]
        
        # Create Course: VIRTUAL ROCKSTAR™
        course, created = Course.objects.get_or_create(
            slug='virtual-rockstar',
            defaults={
                'name': 'VIRTUAL ROCKSTAR™',
                'course_type': 'sprint',
                'status': 'active',
                'description': 'Master the art of virtual presence and digital impact. Learn live streaming, webinars, podcasts, and community engagement from industry rockstars.',
                'short_description': 'Your complete guide to becoming a Virtual Rockstar. Master live streaming, webinars, podcasts, and community engagement.',
                'coach_name': 'Virtual Rockstar Coach',
                'is_subscribers_only': False,
                'is_accredible_certified': True,
                'has_asset_templates': True,
                'exam_unlock_days': 120,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Course {course.name} already exists'))
            # Clear existing lessons if course exists
            course.lessons.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing lessons'))
        
        # Create Main Module
        main_module, _ = Module.objects.get_or_create(
            course=course,
            name='Virtual Rockstar™',
            defaults={'order': 0, 'description': 'Complete Virtual Rockstar course content'}
        )
        
        # All 12 Lessons from the course
        lessons_data = [
            {
                'title': 'Session #1 - Live Streaming',
                'slug': 'session-1-live-streaming',
                'order': 1,
                'description': 'Learn the fundamentals of live streaming and how to engage your audience in real-time.',
                'vimeo_duration_seconds': 2520,  # 42 minutes
                'video_duration': 42,
            },
            {
                'title': 'Smaller Podcast Studio Walk Through',
                'slug': 'smaller-podcast-studio-walk-through',
                'order': 2,
                'description': 'Get a complete walkthrough of setting up a professional podcast studio on any budget.',
                'vimeo_duration_seconds': 1800,  # 30 minutes
                'video_duration': 30,
            },
            {
                'title': 'Session #2 - Webinars',
                'slug': 'session-2-webinars',
                'order': 3,
                'description': 'Master the art of creating and hosting high-converting webinars that build your audience and drive sales.',
                'vimeo_duration_seconds': 2700,  # 45 minutes
                'video_duration': 45,
            },
            {
                'title': 'Session #3 - Challenges',
                'slug': 'session-3-challenges',
                'order': 4,
                'description': 'Learn how to create and run engaging challenges that build community and drive results.',
                'vimeo_duration_seconds': 2400,  # 40 minutes
                'video_duration': 40,
            },
            {
                'title': 'Session #4 - Community Engagement Techniques',
                'slug': 'session-4-community-engagement-techniques',
                'order': 5,
                'description': 'Discover proven techniques for building and engaging a thriving online community.',
                'vimeo_duration_seconds': 2100,  # 35 minutes
                'video_duration': 35,
            },
            {
                'title': 'Session #5 - Podcast & Social Audio',
                'slug': 'session-5-podcast-social-audio',
                'order': 6,
                'description': 'Master podcasting and social audio platforms to expand your reach and build authority.',
                'vimeo_duration_seconds': 2400,  # 40 minutes
                'video_duration': 40,
            },
            {
                'title': 'Session #6 - Summits',
                'slug': 'session-6-summits',
                'order': 7,
                'description': 'Learn how to create and host virtual summits that position you as an industry leader.',
                'vimeo_duration_seconds': 2700,  # 45 minutes
                'video_duration': 45,
            },
            {
                'title': 'Session #7 - Create an Impact - Bonus Session with Alessia Minkus',
                'slug': 'session-7-create-impact-bonus-alessia-minkus',
                'order': 8,
                'description': 'A special bonus session with Alessia Minkus on creating lasting impact in your virtual presence.',
                'vimeo_duration_seconds': 1800,  # 30 minutes
                'video_duration': 30,
            },
            {
                'title': 'Powerful Presence Workshop with Michael Visconti',
                'slug': 'powerful-presence-workshop-michael-visconti',
                'order': 9,
                'description': 'Develop a powerful presence that captivates your audience with Michael Visconti.',
                'vimeo_duration_seconds': 3600,  # 60 minutes
                'video_duration': 60,
            },
            {
                'title': 'High Ticket Creation Workshop with Alessia Minkus',
                'slug': 'high-ticket-creation-workshop-alessia-minkus',
                'order': 10,
                'description': 'Learn how to create and sell high-ticket offers that transform your business with Alessia Minkus.',
                'vimeo_duration_seconds': 3600,  # 60 minutes
                'video_duration': 60,
            },
            {
                'title': 'Zero Dollar Traffic Bootcamp with Kane Minkus',
                'slug': 'zero-dollar-traffic-bootcamp-kane-minkus',
                'order': 11,
                'description': 'Master zero-cost traffic strategies that fill your funnels without spending on ads with Kane Minkus.',
                'vimeo_duration_seconds': 3600,  # 60 minutes
                'video_duration': 60,
            },
            {
                'title': 'Copy Writing Intensive',
                'slug': 'copy-writing-intensive',
                'order': 12,
                'description': 'Master the art of copywriting that converts and sells your offers effortlessly.',
                'vimeo_duration_seconds': 2700,  # 45 minutes
                'video_duration': 45,
            },
        ]
        
        # Create all lessons with Google Drive URLs
        for index, lesson_data in enumerate(lessons_data):
            # Get corresponding Google Drive URL (using first 12 videos for 12 lessons)
            google_drive_url = GOOGLE_DRIVE_VIDEOS[index] if index < len(GOOGLE_DRIVE_VIDEOS) else ""
            
            lesson, created = Lesson.objects.get_or_create(
                course=course,
                slug=lesson_data['slug'],
                defaults={
                    'module': main_module,
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

This session is part of the Virtual Rockstar™ program, designed to help you master virtual presence and digital impact. You'll learn practical strategies, implement key frameworks, and walk away with tangible outputs that move your business forward.

By the end of this session, you'll have actionable insights and a clear path to implementation.''',
                    'ai_outcomes': [
                        'Clear action plan for immediate implementation',
                        'Key frameworks and strategies from the session',
                        'Personalized insights tailored to your offer',
                        'Next steps checklist for continued progress'
                    ],
                    'ai_coach_actions': [
                        'Summarize in 5 bullets',
                        'Turn this into a 3-step action plan',
                        'Generate 3 email hooks from this content',
                        'Give me a comprehension quiz'
                    ],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {lesson.title}'))
            else:
                # Always update existing lesson with Google Drive URL and other data
                lesson.google_drive_url = google_drive_url
                lesson.google_drive_id = google_drive_url.split('/d/')[1].split('/')[0] if '/d/' in google_drive_url else ''
                lesson.vimeo_duration_seconds = lesson_data['vimeo_duration_seconds']
                lesson.video_duration = lesson_data['video_duration']
                lesson.description = lesson_data['description']
                lesson.order = lesson_data['order']
                lesson.save()
                self.stdout.write(self.style.WARNING(f'  ↻ Updated lesson: {lesson.title} with video URL'))

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding completed!'))
        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary:'))
        self.stdout.write(self.style.SUCCESS(f'   - Course: {course.name}'))
        self.stdout.write(self.style.SUCCESS(f'   - Lessons: {Lesson.objects.filter(course=course).count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - All lessons use Google Drive videos'))
        self.stdout.write(self.style.SUCCESS(f'   - 12 unique videos matched to 12 lessons'))
        self.stdout.write(self.style.SUCCESS(f'\n🔗 Access your course:'))
        self.stdout.write(self.style.SUCCESS(f'   Dashboard: http://127.0.0.1:8000/dashboard/'))
        self.stdout.write(self.style.SUCCESS(f'   Course: http://127.0.0.1:8000/courses/{course.slug}/'))
