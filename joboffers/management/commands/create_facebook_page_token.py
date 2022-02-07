import json

import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a facebook page token using a short lived user token.'

    def add_arguments(self, parser):
        parser.add_argument('--client-secret', type=str)
        parser.add_argument('--client-id', type=int)
        parser.add_argument('--page-id', type=int)
        parser.add_argument('--user-token', type=str)

    def handle(self, *args, **options):
        page_id = options.get('page_id')
        short_lived_user_token = options.get('user_token')
        client_id = options.get('client_id')
        client_secret = options.get('client_secret')
        url = (
            f'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&'
            f'client_id={client_id}&'
            f'client_secret={client_secret}&'
            f'fb_exchange_token={short_lived_user_token}'
        )
        result = requests.get(url)
        data = json.loads(result.text)

        long_lived_user_access_token = data.get('access_token')
        url = (
            f'https://graph.facebook.com/{page_id}?fields=access_token&access_token='
            f'{long_lived_user_access_token}'
        )
        result = requests.get(url)
        data = json.loads(result.text)

        long_lived_page_access_token = data.get('access_token')
        self.stdout.write(('\nPor favor, copiá el token y pegalo en el archivo .env o su '
                          'equivalente para el entorno de producción:'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nFACEBOOK_PAGE_ACCESS_TOKEN={long_lived_page_access_token}'
            )
        )
