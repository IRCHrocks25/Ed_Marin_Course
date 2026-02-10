from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myApp.models import Course, Module, Lesson
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Seed the database with courses for Positive Psychology, NLP, Nutrition, Naturopathy, Hypnotherapy, Ayurveda, Art Therapy, and Aroma Therapy'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed course types...'))
        
        # Define course types and their details
        course_types_data = [
            {
                'course_type': 'positive_psychology',
                'name': 'Positive Psychology',
                'description': 'Discover the science of happiness and well-being. Learn evidence-based strategies to cultivate positive emotions, build resilience, and create a flourishing life. This comprehensive course explores the principles of positive psychology, from gratitude practices to strengths-based living.',
                'short_description': 'Master the science of happiness and well-being with evidence-based positive psychology strategies.',
                'coach_name': 'Positive Psychology Coach',
            },
            {
                'course_type': 'nlp',
                'name': 'Neuro-Linguistic Programming (NLP)',
                'description': 'Transform your communication, mindset, and behavior patterns through Neuro-Linguistic Programming. Learn powerful techniques for personal development, improved relationships, and achieving your goals. Master the art of modeling excellence and creating lasting change.',
                'short_description': 'Master NLP techniques to transform your communication, mindset, and achieve your goals.',
                'coach_name': 'NLP Master Coach',
            },
            {
                'course_type': 'nutrition',
                'name': 'Nutrition & Wellness',
                'description': 'Build a foundation of nutritional knowledge that supports optimal health and vitality. Learn about macronutrients, micronutrients, meal planning, and how to make informed food choices that fuel your body and mind. Discover the connection between nutrition and overall well-being.',
                'short_description': 'Learn evidence-based nutrition principles to support optimal health and vitality.',
                'coach_name': 'Nutrition Coach',
            },
            {
                'course_type': 'naturopathy',
                'name': 'Naturopathic Medicine',
                'description': 'Explore natural healing approaches and holistic health principles. Learn about herbal medicine, lifestyle medicine, and natural therapies that support the body\'s innate healing capacity. Understand how to integrate naturopathic principles into your wellness journey.',
                'short_description': 'Discover natural healing approaches and holistic health principles for optimal wellness.',
                'coach_name': 'Naturopathic Practitioner',
            },
            {
                'course_type': 'hypnotherapy',
                'name': 'Hypnotherapy & Mind-Body Connection',
                'description': 'Unlock the power of your subconscious mind through hypnotherapy techniques. Learn how to access deeper states of consciousness for healing, personal transformation, and behavior change. Master self-hypnosis and therapeutic applications of hypnosis.',
                'short_description': 'Master hypnotherapy techniques to unlock your subconscious mind for healing and transformation.',
                'coach_name': 'Hypnotherapy Practitioner',
            },
            {
                'course_type': 'ayurveda',
                'name': 'Ayurveda: Ancient Wisdom for Modern Living',
                'description': 'Discover the ancient Indian system of medicine and wellness. Learn about doshas, Ayurvedic principles, dietary guidelines, and lifestyle practices that promote balance and harmony. Integrate timeless wisdom into your modern life for optimal health.',
                'short_description': 'Learn Ayurvedic principles and practices for balanced living and optimal health.',
                'coach_name': 'Ayurvedic Practitioner',
            },
            {
                'course_type': 'art_therapy',
                'name': 'Art Therapy & Creative Expression',
                'description': 'Explore the healing power of creative expression through art therapy. Learn how artistic processes can facilitate emotional healing, self-discovery, and personal growth. Discover techniques for using art as a therapeutic tool for yourself and others.',
                'short_description': 'Discover the healing power of creative expression through art therapy techniques.',
                'coach_name': 'Art Therapy Practitioner',
            },
            {
                'course_type': 'aroma_therapy',
                'name': 'Aromatherapy & Essential Oils',
                'description': 'Master the therapeutic use of essential oils and aromatherapy. Learn about different essential oils, their properties, safe usage, and how to create blends for various wellness purposes. Understand the science and art of aromatherapy for physical and emotional well-being.',
                'short_description': 'Master the therapeutic use of essential oils and aromatherapy for wellness.',
                'coach_name': 'Aromatherapy Practitioner',
            },
        ]
        
        courses_created = 0
        courses_updated = 0
        
        for course_data in course_types_data:
            course_slug = slugify(course_data['name'])
            
            course, created = Course.objects.get_or_create(
                slug=course_slug,
                defaults={
                    'name': course_data['name'],
                    'course_type': course_data['course_type'],
                    'status': 'active',
                    'description': course_data['description'],
                    'short_description': course_data['short_description'],
                    'coach_name': course_data['coach_name'],
                    'is_subscribers_only': False,
                    'is_accredible_certified': True,
                    'has_asset_templates': True,
                    'exam_unlock_days': 90,
                    'visibility': 'public',
                    'enrollment_method': 'open',
                    'access_duration_type': 'lifetime',
                }
            )
            
            if created:
                courses_created += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created course: {course.name}'))
            else:
                courses_updated += 1
                # Update existing course with new data
                course.name = course_data['name']
                course.course_type = course_data['course_type']
                course.description = course_data['description']
                course.short_description = course_data['short_description']
                course.coach_name = course_data['coach_name']
                course.status = 'active'
                course.save()
                self.stdout.write(self.style.WARNING(f'↻ Updated course: {course.name}'))
            
            # Create a default module for each course
            module, module_created = Module.objects.get_or_create(
                course=course,
                name='Module 1',
                defaults={
                    'order': 1,
                    'description': f'Introduction to {course_data["name"]} - foundational concepts and principles.'
                }
            )
            
            if module_created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created module: {module.name}'))
            else:
                self.stdout.write(f'  Module already exists: {module.name}')
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ Course types seeding completed!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary:'))
        self.stdout.write(self.style.SUCCESS(f'   - Courses created: {courses_created}'))
        self.stdout.write(self.style.SUCCESS(f'   - Courses updated: {courses_updated}'))
        self.stdout.write(self.style.SUCCESS(f'   - Total courses: {courses_created + courses_updated}'))
        self.stdout.write(self.style.SUCCESS(f'\n🔗 Access your courses:'))
        self.stdout.write(self.style.SUCCESS(f'   All Courses: http://127.0.0.1:8000/courses/'))
        self.stdout.write(self.style.SUCCESS(f'\n💡 Next Steps:'))
        self.stdout.write(self.style.SUCCESS(f'   Use the webhook endpoint to generate content:'))
        self.stdout.write(self.style.SUCCESS(f'   POST /api/generate-course-content/'))
        self.stdout.write(self.style.SUCCESS(f'   With payload: {{"course": "positive_psychology", "module": "Module1"}}'))

