import requests
import urllib.parse

TELEGRAM_API_URL = 'https://api.telegram.org/bot'

#TODO: get BOT_TOKEN and moderators chat_id from settings, these are dummy values
BOT_TOKEN = 'xxxxxnCs'
MODERATORS_CHAT_ID = 9999


def _send_message(message :str, chat_id :int):
    """Send a message to a chat using a bot."""
    safe_message = urllib.parse.quote_plus(message)
    url = f'{TELEGRAM_API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={safe_message}'
    status = requests.get(url)
    return status


def send_notification_to_moderators(job_slug :str):
    """Send a notification of a slug thats needs to be moderated to moderator's group."""
    complete_offer_slug_url = f'https://www.python.org.ar/trabajo-nueva/admin/{job_slug}'
    moderation_message = f'La oferta {complete_offer_slug_url} necesita ser moderada.'
    status = _send_message(moderation_message, MODERATORS_CHAT_ID)
    print(status)


if __name__=='__main__':
    job_slug = 'trabajito-python'
    send_notification_to_moderators(job_slug)
