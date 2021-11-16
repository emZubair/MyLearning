from logging import getLogger
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from prac_models.models import Book

log = getLogger(__name__)


class Command(BaseCommand):
    """
    A management command to create Course Authors grouop
    """

    help = "Create a course authors group"

    def handle(self, *args, **options):
        log.info("Creating Course Authors Group")
        course_authors, created = Group.objects.get_or_create(name='CA')
        can_view_book = Permission.objects.get(codename='view_author')
        # ct = ContentType.objects.get_for_model(Book)
        import pdb
        pdb.set_trace()
        # permission, _ = Permission.objects.get_or_create(codename='can_add_book',
        #                                               name='Can add books',
        #                                               content_type=ct)
        course_authors.permissions.add(can_view_book)

