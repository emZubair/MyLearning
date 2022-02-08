from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from django.db.models import Count


class Command(BaseCommand):
    help = ''' Send an email reminder to students who haven't enrolled
                in any courses yet.
    '''

    def add_arguments(self, parser):
        parser.add_argument('--days', dest='days', type=int)

    def handle(self, *args, **options):
        emails = []
        subject = 'Enroll in a Course'
        date_joined = timezone.now().today() - timedelta(days=options.get('days', 10))
        users = User.objects.annotate(course_count=Count('courses_joined')).filter(
            course_count=0, date_joined__date__lte=date_joined)

        for user in users:
            message = """
            Dear {},
            We noticed that you didn't enroll any courses yet. 
            What are you waiting for? If can't find the course of your choice, write back to us.
            """.format(user.first_name)

            emails.append(
                (subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            )
        # send_mass_mail(emails)
        self.stdout.write('sent {} reminders'.format(len(emails)))

