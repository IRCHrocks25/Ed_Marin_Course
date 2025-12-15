from django.core.management.base import BaseCommand
from myApp.models import Course, Lesson, LessonQuiz, LessonQuizQuestion


class Command(BaseCommand):
    help = "Seed a sample quiz (with questions) for Virtual Rockstar™ Lesson 1 only"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Seeding Lesson 1 quiz..."))

        # Find the Virtual Rockstar course and lesson 1
        try:
            course = Course.objects.get(slug="virtual-rockstar")
        except Course.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    '✗ Course with slug "virtual-rockstar" not found. Run seed_data first.'
                )
            )
            return

        try:
            lesson1 = Lesson.objects.get(course=course, slug="session-1-live-streaming")
        except Lesson.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    '✗ Lesson 1 with slug "session-1-live-streaming" not found.'
                )
            )
            return

        quiz, created_quiz = LessonQuiz.objects.get_or_create(
            lesson=lesson1,
            defaults={
                "title": "Session #1 – Live Streaming Quiz",
                "description": "Quick check of the core concepts from Session #1.",
                "passing_score": 80,
                "is_required": False,
            },
        )

        if created_quiz:
            self.stdout.write(self.style.SUCCESS("  ✓ Created quiz for Lesson 1"))
        else:
            self.stdout.write(
                self.style.WARNING("  ↻ Quiz for Lesson 1 already exists (reusing it)")
            )

        # Only seed questions if none exist yet
        if not quiz.questions.exists():
            LessonQuizQuestion.objects.create(
                quiz=quiz,
                text="What is the primary goal of a live streaming session in Virtual Rockstar™?",
                option_a="To perfectly deliver a scripted presentation",
                option_b="To create real-time engagement and connection with your audience",
                option_c="To test your camera and microphone settings",
                option_d="To sell as many products as possible in the first 5 minutes",
                correct_option="B",
                order=1,
            )
            LessonQuizQuestion.objects.create(
                quiz=quiz,
                text="Which of these is MOST important for keeping viewers engaged live?",
                option_a="Reading your slides word for word",
                option_b="Using only pre-recorded content",
                option_c="Asking questions and responding to comments in real time",
                option_d="Having the most expensive camera setup",
                correct_option="C",
                order=2,
            )
            LessonQuizQuestion.objects.create(
                quiz=quiz,
                text="Before you go live, what should you always do?",
                option_a="Memorize your script line by line",
                option_b="Clarify the single main outcome you want for your viewers",
                option_c="Disable the chat so you are not distracted",
                option_d="Schedule 5 different streams at the same time",
                correct_option="B",
                order=3,
            )
            self.stdout.write(
                self.style.SUCCESS("  ✓ Seeded 3 quiz questions for Lesson 1")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "  ↻ Quiz already has questions – not adding duplicates"
                )
            )

        self.stdout.write(self.style.SUCCESS("✅ Lesson 1 quiz seeding complete."))


