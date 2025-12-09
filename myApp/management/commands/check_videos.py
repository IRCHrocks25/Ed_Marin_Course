from django.core.management.base import BaseCommand
from myApp.models import Lesson


class Command(BaseCommand):
    help = 'Check video settings for all lessons'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking video settings...\n'))
        
        lessons = Lesson.objects.all()
        
        if not lessons.exists():
            self.stdout.write(self.style.ERROR('No lessons found! Run seed_data first.'))
            return
        
        for lesson in lessons:
            self.stdout.write(f'\n📹 {lesson.title}')
            self.stdout.write(f'   Course: {lesson.course.name}')
            
            if lesson.google_drive_url:
                self.stdout.write(self.style.SUCCESS(f'   ✅ Google Drive: {lesson.google_drive_url[:60]}...'))
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  Google Drive URL: NOT SET'))
            
            if lesson.vimeo_id:
                self.stdout.write(self.style.WARNING(f'   ⚠️  Vimeo ID: {lesson.vimeo_id} (will be ignored if Google Drive exists)'))
            else:
                self.stdout.write('   ℹ️  Vimeo ID: Not set')
            
            if lesson.video_url:
                self.stdout.write(f'   ℹ️  Video URL: {lesson.video_url[:60]}...')
            
            # Determine what will be used
            if lesson.google_drive_url:
                self.stdout.write(self.style.SUCCESS('   → Will use: Google Drive ✅'))
            elif lesson.vimeo_id:
                self.stdout.write(self.style.WARNING('   → Will use: Vimeo (but may not work)'))
            elif lesson.video_url:
                self.stdout.write('   → Will use: Generic video URL')
            else:
                self.stdout.write(self.style.ERROR('   → Will show: Placeholder (no video!)'))
        
        self.stdout.write(self.style.SUCCESS(f'\n\n✅ Checked {lessons.count()} lessons'))

