from django.core.management.base import BaseCommand
from django.utils import timezone
from cvcl.models import Environment


class Command(BaseCommand):
    help = 'Cleans Environments for expired Assignments'

    def handle(self, *args, **options):
        for environment in Environment.objects.filter(assignment__end_date__lt=timezone.now()):
            if environment.user != environment.assignment.course.instructor:
                environment.delete()
                self.stdout.write(
                    self.style.SUCCESS('Deleted expired environment for assignment %s in course %s, user: %s' % (
                        environment.assignment, environment.assignment.course, environment.user)))
