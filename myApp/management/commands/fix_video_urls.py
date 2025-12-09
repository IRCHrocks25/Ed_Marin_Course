from django.core.management.base import BaseCommand
from django.db.models import Q
from myApp.models import Lesson, Course


class Command(BaseCommand):
    help = 'Fix missing video URLs for lessons'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking lessons for missing video URLs...'))
        
        # Google Drive video URLs (embed format) - matching seed_data.py (12 unique videos)
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
        
        # Get Virtual Rockstar course
        try:
            course = Course.objects.get(slug='virtual-rockstar')
        except Course.DoesNotExist:
            self.stdout.write(self.style.ERROR('Virtual Rockstar course not found. Run seed_data first.'))
            return
        
        # Get all lessons for this course, ordered by order field
        lessons = Lesson.objects.filter(course=course).order_by('order')
        
        fixed_count = 0
        for index, lesson in enumerate(lessons):
            # Check if lesson is missing video URL
            has_video = lesson.google_drive_url or lesson.vimeo_id or lesson.video_url
            
            if not has_video and index < len(GOOGLE_DRIVE_VIDEOS):
                google_drive_url = GOOGLE_DRIVE_VIDEOS[index]
                lesson.google_drive_url = google_drive_url
                lesson.google_drive_id = google_drive_url.split('/d/')[1].split('/')[0] if '/d/' in google_drive_url else ''
                lesson.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Fixed: {lesson.title}'))
                fixed_count += 1
            elif not has_video:
                self.stdout.write(self.style.WARNING(f'  ⚠ No video available for: {lesson.title} (index {index})'))
        
        if fixed_count > 0:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Fixed {fixed_count} lesson(s) with video URLs!'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ All lessons already have video URLs.'))
        
        # Show summary
        total_lessons = lessons.count()
        lessons_with_video = lessons.filter(
            Q(google_drive_url__isnull=False) | 
            Q(vimeo_id__isnull=False) | 
            Q(video_url__isnull=False)
        ).exclude(
            google_drive_url='', 
            vimeo_id='', 
            video_url=''
        ).count()
        
        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary: {lessons_with_video}/{total_lessons} lessons have video URLs'))

