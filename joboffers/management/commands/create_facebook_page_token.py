"""
This command is needed in order to create a valid facebook page token.

Steps:

1. First go to developers.facebook.com and create an app, you will need later the
    client_id and client_secret for that app.
2. Then go to the api explorer https://developers.facebook.com/tools/explorer/ select the
    newly created application, then select "Get User Token" and add the following permissions:
    - pages_show_list
    - publish_to_groups
    - pages_read_engagement
    - pages_manage_post
    public_profile will be automatically selected.
3. Then click on Generate Token. It will pop up a window when you will select wich page would you
    want this app to be valid for. After that, facebook will display a message saying that the app
    would need to go under revision, you can safely ignore that.
4. Finish the process and then copy the token as you will need it later.
5. Go to the Pyar's facebook page and in the about dialog you will find the page id of the site
   you'll need to copy that as well.
6. Finally run this command.

What does this command do?
==========================

The token generated from the facebook console, is a Short lived User Token. It last only 60 minutes
and is not usefull to post to pages. To do that, you will need a Page Token. The one that can be
generated on the console is also a short lived token, so in order tu have a token that does not
expire, you need a Short Lived User Token that using the api is swapped with a Long lived user
token (valid for 60 days) and you can use that token later to obtain the Long Lived page token.

To test the validity of the token, you can past it here:

https://developers.facebook.com/tools/debug/accesstoken/


Running the command
===================
python manage.py create_facebook_page_token --page-id={page_id} \
    --client-id={client_id}--client-secret={client_secret} \
    --user-token={short_livedf_user_token}

This wil output the following:
FACEBOOK_PAGE_ACCESS_TOKEN=TOKEN

This value will have to be pasted into the .env file on development, or added to the enviroment
in staging or production mode alongside with the FACEBOOK_PAGE_ID.
"""
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
