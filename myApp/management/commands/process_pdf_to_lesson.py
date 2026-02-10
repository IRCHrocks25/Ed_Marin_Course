"""
Management command to process PDF files and generate lesson content using AI.

Usage:
    # Process a single PDF file
    python manage.py process_pdf_to_lesson \
        --course positive_psychology \
        --module "Module 1" \
        --pdf-path "courses/positive_psychology/module1/lesson1.pdf" \
        --lesson-title "Introduction to Positive Psychology"

    # Process entire folder
    python manage.py process_pdf_to_lesson \
        --course positive_psychology \
        --module "Module 1" \
        --folder-path "courses/positive_psychology/module1/"

    # Process with auto-splitting (for large PDFs)
    python manage.py process_pdf_to_lesson \
        --course positive_psychology \
        --module "Module 1" \
        --pdf-path "courses/positive_psychology/module1_complete.pdf" \
        --split-by-pages 10
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from django.db.models import Max
from myApp.models import Course, Module, Lesson
from myApp.utils.pdf_extractor import PDFExtractor
from myApp.utils.ai_content_generator import AIContentGenerator
import os
import glob


class Command(BaseCommand):
    help = 'Process PDF files and generate lesson content using AI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--course',
            type=str,
            required=True,
            help='Course type (e.g., positive_psychology, nlp, nutrition)'
        )
        parser.add_argument(
            '--module',
            type=str,
            required=True,
            help='Module name (e.g., "Module 1", "Introduction")'
        )
        parser.add_argument(
            '--pdf-path',
            type=str,
            help='Path to a single PDF file to process'
        )
        parser.add_argument(
            '--folder-path',
            type=str,
            help='Path to folder containing PDF files to process'
        )
        parser.add_argument(
            '--lesson-title',
            type=str,
            help='Suggested title for the lesson (optional)'
        )
        parser.add_argument(
            '--split-by-pages',
            type=int,
            help='Split PDF into multiple lessons by page count (e.g., 10 = every 10 pages)'
        )
        parser.add_argument(
            '--skip-ai',
            action='store_true',
            help='Skip AI generation, just extract text and create basic lessons'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating lessons'
        )

    def handle(self, *args, **options):
        course_type = options['course']
        module_name = options['module']
        pdf_path = options.get('pdf_path')
        folder_path = options.get('folder_path')
        lesson_title = options.get('lesson_title')
        split_by_pages = options.get('split_by_pages')
        skip_ai = options.get('skip_ai', False)
        dry_run = options.get('dry_run', False)

        # Validate inputs
        if not pdf_path and not folder_path:
            raise CommandError('Either --pdf-path or --folder-path must be provided')

        # Initialize PDF extractor
        try:
            pdf_extractor = PDFExtractor()
        except ImportError as e:
            raise CommandError(str(e))

        # Initialize AI generator (if not skipping)
        ai_generator = None
        if not skip_ai:
            try:
                ai_generator = AIContentGenerator()
            except (ImportError, ValueError) as e:
                self.stdout.write(self.style.WARNING(
                    f'AI generation not available: {e}\n'
                    'Falling back to basic text extraction.'
                ))
                skip_ai = True

        # Get or create course
        course = self._get_or_create_course(course_type, dry_run)
        if not dry_run and not course:
            raise CommandError(f'Failed to create course: {course_type}')

        # Get or create module
        module = self._get_or_create_module(course, module_name, dry_run)
        if not dry_run and not module:
            raise CommandError(f'Failed to create module: {module_name}')

        # Process PDFs
        pdf_files = []
        if pdf_path:
            if not os.path.exists(pdf_path):
                raise CommandError(f'PDF file not found: {pdf_path}')
            pdf_files = [pdf_path]
        elif folder_path:
            if not os.path.exists(folder_path):
                raise CommandError(f'Folder not found: {folder_path}')
            pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))
            if not pdf_files:
                raise CommandError(f'No PDF files found in: {folder_path}')

        self.stdout.write(self.style.SUCCESS(
            f'\nProcessing {len(pdf_files)} PDF file(s)...\n'
        ))

        lessons_created = 0
        lessons_updated = 0

        for pdf_file in pdf_files:
            self.stdout.write(f'Processing: {os.path.basename(pdf_file)}')
            
            try:
                if split_by_pages:
                    # Split PDF into multiple lessons
                    chunks = pdf_extractor.extract_by_pages(pdf_file, split_by_pages)
                    self.stdout.write(f'  Split into {len(chunks)} lesson(s)')
                    
                    for i, chunk in enumerate(chunks, 1):
                        lesson_num = i
                        suggested_title = f"{lesson_title or 'Lesson'} {lesson_num}" if lesson_title else f"Lesson {lesson_num}"
                        
                        created, updated = self._process_pdf_chunk(
                            course, module, chunk['text'], suggested_title,
                            ai_generator, skip_ai, dry_run, course_type, module_name
                        )
                        lessons_created += created
                        lessons_updated += updated
                else:
                    # Process entire PDF as single lesson
                    pdf_text = pdf_extractor.extract_text(pdf_file)
                    suggested_title = lesson_title or os.path.splitext(os.path.basename(pdf_file))[0]
                    
                    created, updated = self._process_pdf_chunk(
                        course, module, pdf_text, suggested_title,
                        ai_generator, skip_ai, dry_run, course_type, module_name
                    )
                    lessons_created += created
                    lessons_updated += updated
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'  Error processing {pdf_file}: {str(e)}'
                ))
                continue

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ PDF Processing Completed!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary:'))
        self.stdout.write(self.style.SUCCESS(f'   - Lessons created: {lessons_created}'))
        self.stdout.write(self.style.SUCCESS(f'   - Lessons updated: {lessons_updated}'))
        if dry_run:
            self.stdout.write(self.style.WARNING('\n⚠️  DRY RUN - No lessons were actually created'))

    def _get_or_create_course(self, course_type, dry_run=False):
        """Get or create course"""
        try:
            course = Course.objects.get(course_type=course_type)
            if not dry_run:
                self.stdout.write(f'Found existing course: {course.name}')
            return course
        except Course.DoesNotExist:
            # Try to find by slug
            course_slug = slugify(course_type.replace('_', ' '))
            try:
                course = Course.objects.get(slug=course_slug)
                if not dry_run:
                    self.stdout.write(f'Found existing course: {course.name}')
                return course
            except Course.DoesNotExist:
                if dry_run:
                    self.stdout.write(f'Would create course: {course_type}')
                    return None
                
                # Create course
                course_name = course_type.replace('_', ' ').title()
                course = Course.objects.create(
                    slug=course_slug,
                    name=course_name,
                    course_type=course_type,
                    status='active',
                    description=f'Course content for {course_name}',
                    short_description=f'Learn {course_name}',
                    visibility='public',
                    enrollment_method='open',
                    access_duration_type='lifetime',
                )
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.name}'))
                return course

    def _get_or_create_module(self, course, module_name, dry_run=False):
        """Get or create module"""
        try:
            module = Module.objects.get(course=course, name=module_name)
            if not dry_run:
                self.stdout.write(f'Found existing module: {module.name}')
            return module
        except Module.DoesNotExist:
            if dry_run:
                self.stdout.write(f'Would create module: {module_name}')
                return None
            
            # Get next order number
            max_order = Module.objects.filter(course=course).aggregate(
                max_order=Max('order')
            )['max_order'] or 0
            
            module = Module.objects.create(
                course=course,
                name=module_name,
                order=max_order + 1,
                description=f'Module content for {module_name}'
            )
            self.stdout.write(self.style.SUCCESS(f'Created module: {module.name}'))
            return module

    def _process_pdf_chunk(
        self, course, module, pdf_text, suggested_title,
        ai_generator, skip_ai, dry_run, course_name, module_name
    ):
        """Process a PDF text chunk and create/update lesson"""
        created = 0
        updated = 0

        if dry_run:
            self.stdout.write(f'  Would create lesson: {suggested_title}')
            return 0, 0

        # Generate lesson slug
        lesson_slug = slugify(suggested_title)
        
        # Get next order number
        max_order = Lesson.objects.filter(course=course, module=module).aggregate(
            max_order=Max('order')
        )['max_order'] or 0

        if skip_ai or not ai_generator:
            # Create basic lesson without AI generation
            lesson, was_created = Lesson.objects.get_or_create(
                course=course,
                module=module,
                slug=lesson_slug,
                defaults={
                    'title': suggested_title,
                    'description': pdf_text[:500] + '...' if len(pdf_text) > 500 else pdf_text,
                    'order': max_order + 1,
                    'lesson_type': 'video',
                    'ai_generation_status': 'pending',
                }
            )
            
            if was_created:
                created = 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {lesson.title}'))
            else:
                updated = 1
                self.stdout.write(self.style.WARNING(f'  ↻ Updated lesson: {lesson.title}'))
        else:
            # Generate AI content
            try:
                self.stdout.write(f'  Generating AI content...')
                ai_content = ai_generator.generate_lesson_content(
                    pdf_text=pdf_text,
                    course_name=course_name,
                    module_name=module_name,
                    suggested_title=suggested_title
                )
                
                # Convert content blocks to Editor.js format
                editorjs_content = ai_generator.convert_to_editorjs_format(
                    ai_content['content_blocks']
                )
                
                # Create or update lesson
                lesson, was_created = Lesson.objects.get_or_create(
                    course=course,
                    module=module,
                    slug=lesson_slug,
                    defaults={
                        'title': ai_content['clean_title'],
                        'description': ai_content['full_description'],
                        'order': max_order + 1,
                        'lesson_type': 'video',
                        'content': editorjs_content,
                        'ai_generation_status': 'generated',
                        'ai_clean_title': ai_content['clean_title'],
                        'ai_short_summary': ai_content['short_summary'],
                        'ai_full_description': ai_content['full_description'],
                        'ai_outcomes': ai_content['outcomes'],
                        'ai_coach_actions': ai_content['coach_actions'],
                    }
                )
                
                if was_created:
                    created = 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {lesson.title}'))
                else:
                    # Update existing lesson
                    lesson.title = ai_content['clean_title']
                    lesson.description = ai_content['full_description']
                    lesson.content = editorjs_content
                    lesson.ai_generation_status = 'generated'
                    lesson.ai_clean_title = ai_content['clean_title']
                    lesson.ai_short_summary = ai_content['short_summary']
                    lesson.ai_full_description = ai_content['full_description']
                    lesson.ai_outcomes = ai_content['outcomes']
                    lesson.ai_coach_actions = ai_content['coach_actions']
                    lesson.save()
                    updated = 1
                    self.stdout.write(self.style.WARNING(f'  ↻ Updated lesson: {lesson.title}'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'  Error generating AI content: {str(e)}'
                ))
                # Fall back to basic lesson creation
                lesson, was_created = Lesson.objects.get_or_create(
                    course=course,
                    module=module,
                    slug=lesson_slug,
                    defaults={
                        'title': suggested_title,
                        'description': pdf_text[:500] + '...' if len(pdf_text) > 500 else pdf_text,
                        'order': max_order + 1,
                        'lesson_type': 'video',
                        'ai_generation_status': 'pending',
                    }
                )
                if was_created:
                    created = 1
                else:
                    updated = 1

        return created, updated

