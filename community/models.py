from allauth.account.signals import user_signed_up
from waliki.models import ACLRule
from django.contrib.auth.models import Permission
from waliki.settings import get_slug
from django.dispatch import receiver


@receiver(user_signed_up)
def create_acl_for_user_wiki_own_page(sender, **kwargs):
    user = kwargs['user']
    perms = Permission.objects.filter(content_type__app_label='waliki',
                                      codename__in=('add_page', 'change_page')).values_list(
        'id', flat=True)

    rule, created = ACLRule.objects.get_or_create(name='pagina propia {}'.format(str(user)),
                              slug='miembros/{}'.format(
                                  get_slug(user.username)),
                              apply_to=ACLRule.TO_EXPLICIT_LIST,
                              as_namespace=True
                              )
    if created:
        rule.permissions.add(*perms)
        rule.users.add(user)
