def pyar_wiki_url(request):
    from django.conf import settings
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'PYAR_WIKI_URL': settings.PYAR_WIKI_URL}
