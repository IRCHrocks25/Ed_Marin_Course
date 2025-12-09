from django.core.management.base import BaseCommand
from myApp.models import Lesson


class Command(BaseCommand):
    help = 'Add Google Drive URL to lessons'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='Google Drive embed URL (e.g., https://drive.google.com/file/d/FILE_ID/preview)')
        parser.add_argument('--lesson-id', type=int, help='Specific lesson ID to update (optional)')

    def handle(self, *args, **options):
        google_drive_url = options.get('url')
        lesson_id = options.get('lesson_id')
        
        if not google_drive_url:
            self.stdout.write(self.style.ERROR('Please provide --url argument'))
            self.stdout.write(self.style.WARNING('Example: python manage.py add_google_drive --url "https://drive.google.com/file/d/FILE_ID/preview"'))
            return
        
        if lesson_id:
            # Update specific lesson
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                lesson.google_drive_url = google_drive_url
                lesson.save()
                self.stdout.write(self.style.SUCCESS(f'Updated lesson: {lesson.title}'))
            except Lesson.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Lesson with ID {lesson_id} not found'))
        else:
            # Update all lessons
            lessons = Lesson.objects.all()
            updated_count = 0
            for lesson in lessons:
                lesson.google_drive_url = google_drive_url
                lesson.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Updated: {lesson.title}'))
            
            self.stdout.write(self.style.SUCCESS(f'\n✅ Updated {updated_count} lessons with Google Drive URL'))

