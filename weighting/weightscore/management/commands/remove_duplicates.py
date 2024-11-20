from django.core.management.base import BaseCommand
from django.db.models import Max
from weightscore.models import ExamScore  # Update with your app name and model

class Command(BaseCommand):
    help = "Remove duplicate ExamScore records and keep the most recent"

    def handle(self, *args, **kwargs):
        self.stdout.write("Identifying duplicate records...")

        # Step 1: Identify duplicate groups
        duplicate_groups = (
            ExamScore.objects
            .values('employee', 'exam', 'score')  # Group by employee, exam, and score
            .annotate(latest_date=Max('exam_date'))  # Get the latest exam_date
        )

        # Step 2: Remove older duplicates
        duplicates_removed = 0
        for group in duplicate_groups:
            employee = group['employee']
            exam = group['exam']
            score = group['score']
            latest_date = group['latest_date']

            # Find all duplicates for this group
            duplicates = ExamScore.objects.filter(
                employee=employee,
                exam=exam,
                score=score
            )

            # Exclude the most recent record
            duplicates_to_delete = duplicates.exclude(exam_date=latest_date)

            # Count and delete duplicates
            duplicates_removed += duplicates_to_delete.count()
            duplicates_to_delete.delete()

        self.stdout.write(f"Removed {duplicates_removed} duplicate records.")
