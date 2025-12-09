from django.core.management.base import BaseCommand
from myApp.models import Lesson


class Command(BaseCommand):
    help = 'Clear Vimeo IDs so Google Drive videos will be used instead'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Clearing Vimeo IDs to use Google Drive videos...'))
        
        # Clear vimeo_id for all lessons that have google_drive_url
        lessons = Lesson.objects.filter(google_drive_url__isnull=False).exclude(google_drive_url='')
        
        updated_count = 0
        for lesson in lessons:
            if lesson.vimeo_id:  # Only clear if vimeo_id exists
                lesson.vimeo_id = ''
                lesson.vimeo_url = ''
                lesson.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Cleared Vimeo ID for: {lesson.title}'))
        
        if updated_count == 0:
            self.stdout.write(self.style.WARNING('No lessons found with both Vimeo ID and Google Drive URL'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Cleared Vimeo IDs from {updated_count} lessons'))
            self.stdout.write(self.style.SUCCESS('Google Drive videos will now be used!'))

