from django.core.management.base import BaseCommand

from joboffers.utils import expire_old_offers


class Command(BaseCommand):
    help = 'Queries the database for expired offers and send the mails to the publishers'

    def handle(self, *args, **options):
        expire_old_offers()
