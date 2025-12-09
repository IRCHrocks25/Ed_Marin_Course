from django.core.management.base import BaseCommand
from myApp.models import Lesson


class Command(BaseCommand):
    help = 'Fix Vimeo IDs for existing lessons'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Updating Vimeo IDs...'))
        
        # Your Vimeo video ID
        VIMEO_ID = "884773301"
        VIMEO_URL = f"https://vimeo.com/{VIMEO_ID}"
        
        # Update all lessons that don't have vimeo_id
        lessons = Lesson.objects.filter(vimeo_id__isnull=True) | Lesson.objects.filter(vimeo_id='')
        
        updated_count = 0
        for lesson in lessons:
            lesson.vimeo_id = VIMEO_ID
            lesson.vimeo_url = VIMEO_URL
            lesson.vimeo_thumbnail = f"https://i.vimeocdn.com/video/{VIMEO_ID}_640.jpg"
            lesson.vimeo_duration_seconds = 2520  # 42 minutes
            lesson.save()
            updated_count += 1
            self.stdout.write(self.style.SUCCESS(f'  Updated: {lesson.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Updated {updated_count} lessons with Vimeo ID: {VIMEO_ID}'))
        self.stdout.write(self.style.WARNING('\n⚠️  If you have multiple videos, update each lesson individually with the correct Vimeo ID'))

