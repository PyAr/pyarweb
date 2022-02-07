from django.core.management.base import BaseCommand

from joboffers.telegram_notifier import send_notification_to_moderators


class Command(BaseCommand):
    help = 'Test sending a real notification to telegram.'

    def handle(self, *args, **options):
        response = send_notification_to_moderators('trabajito-python')

        assert response.status_code == 200

        self.stdout.write(self.style.SUCCESS('Mensaje de prueba enviado'))
