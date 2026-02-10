"""
Management command to delete AI-generated lessons.

Usage:
    # Delete all generated lessons from a specific course
    python manage.py delete_generated_lessons --course aromatherapy-essential-oils

    # Delete lessons from a specific module
    python manage.py delete_generated_lessons --course aromatherapy-essential-oils --module "Aromatherapy Training"

    # Delete all generated lessons (all courses)
    python manage.py delete_generated_lessons --all

    # Dry run (preview what would be deleted)
    python manage.py delete_generated_lessons --course aromatherapy-essential-oils --dry-run
"""
from django.core.management.base import BaseCommand, CommandError
from myApp.models import Course, Module, Lesson


class Command(BaseCommand):
    help = 'Delete AI-generated lessons from courses'

    def add_arguments(self, parser):
        parser.add_argument(
            '--course',
            type=str,
            help='Course slug (e.g., aromatherapy-essential-oils)'
        )
        parser.add_argument(
            '--module',
            type=str,
            help='Module name (optional, filters by module)'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Delete all generated lessons from all courses'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )

    def handle(self, *args, **options):
        course_slug = options.get('course')
        module_name = options.get('module')
        delete_all = options.get('all', False)
        dry_run = options.get('dry_run', False)

        if not delete_all and not course_slug:
            raise CommandError('Either --course or --all must be provided')

        if dry_run:
            self.stdout.write(self.style.WARNING('⚠️  DRY RUN MODE - No lessons will be deleted\n'))

        if delete_all:
            # Delete all generated lessons
            lessons = Lesson.objects.filter(ai_generation_status__in=['generated', 'approved'])
            total_count = lessons.count()
            
            if total_count == 0:
                self.stdout.write(self.style.WARNING('No generated lessons found.'))
                return
            
            if dry_run:
                self.stdout.write(f'Would delete {total_count} lesson(s) from all courses:')
                for lesson in lessons[:20]:  # Show first 20
                    self.stdout.write(f'  - {lesson.course.name} > {lesson.module.name if lesson.module else "No Module"} > {lesson.title}')
                if total_count > 20:
                    self.stdout.write(f'  ... and {total_count - 20} more')
            else:
                lessons.delete()
                self.stdout.write(self.style.SUCCESS(f'✅ Deleted {total_count} generated lesson(s) from all courses'))
        else:
            # Delete from specific course
            try:
                course = Course.objects.get(slug=course_slug)
            except Course.DoesNotExist:
                raise CommandError(f'Course not found: {course_slug}')

            # Filter lessons
            lessons = Lesson.objects.filter(
                course=course,
                ai_generation_status__in=['generated', 'approved']
            )

            if module_name:
                try:
                    module = Module.objects.get(course=course, name=module_name)
                    lessons = lessons.filter(module=module)
                    self.stdout.write(f'Filtering by module: {module_name}')
                except Module.DoesNotExist:
                    raise CommandError(f'Module not found: {module_name}')

            total_count = lessons.count()

            if total_count == 0:
                self.stdout.write(self.style.WARNING(f'No generated lessons found in {course.name}'))
                return

            if dry_run:
                self.stdout.write(f'\nWould delete {total_count} lesson(s) from "{course.name}":')
                for lesson in lessons:
                    module_info = f' > {lesson.module.name}' if lesson.module else ''
                    self.stdout.write(f'  - {lesson.title}{module_info}')
            else:
                lesson_titles = [lesson.title for lesson in lessons]
                lessons.delete()
                self.stdout.write(self.style.SUCCESS(f'\n✅ Deleted {total_count} lesson(s) from "{course.name}":'))
                for title in lesson_titles[:10]:  # Show first 10
                    self.stdout.write(f'  - {title}')
                if len(lesson_titles) > 10:
                    self.stdout.write(f'  ... and {len(lesson_titles) - 10} more')

        if dry_run:
            self.stdout.write(self.style.WARNING('\n⚠️  This was a dry run. Use without --dry-run to actually delete.'))

