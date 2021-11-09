from collections import defaultdict
from functools import wraps

from .models import OfferState


#def check_ownership(joboffer, current_editor, permission_required):
#TRANSITIONS_PUBLISHER = defaultdict(dict)
#
#def check_state(valid_states, next_state):
#    def callable(func):
#        @wraps(func)
#        def wrapped(job_offer):
#
#            if job_offer.state not in valid_states:
#                raise ValueError('Inconsistent state')
#            else:
#                result = func(job_offer)
#                return result
#        return wrapped
#
#    return callable
#
# To check for permissions on the view, use the django decorator, pass user test_transition_path\
# Create a function to specifically chec for that
#https://docs.djangoproject.com/es/2.2/_modules/django/contrib/auth/decorators/

def check_state(func):
    @wraps(func)
    def wrapped(job_offer):
        if job_offer.state not in func.valid_prev_states:
            raise ValueError('Inconsistent state')
        else:
            result = func(job_offer)
            return result
    return wrapped


# see how to redirect to a view or call a different function
@check_state
def edit(job_offer):
    print(job_offer)
    return next_state
edit.verbose_name='Editar'
edit.valid_prev_states=(OfferState.DEACTIVATED, OfferState.REJECTED)


def moderate():
    return OfferState.DEACTIVATED


def reactivate():
    return OfferState.DEACTIVATED


def deactivate():
    return OfferState.DEACTIVATED


def aprove():
    return OfferState.DEACTIVATED


@check_state
def reject():
    return OfferState.DEACTIVATED
reject.verbose_name='Rechazar'
reject.valid_prev_states=(OfferState.MODERATION)


TRANSITIONS_PUBLISHER = defaultdict(list)
#TRANSITIONS_ADMIN = defaultdict(dict)

def register_transition(func):
    for state in func.valid_prev_states:
        TRANSITIONS_PUBLISHER[state].append(func)

register_transition(edit)
register_transition(reject)

# To avoid any further magic on accessing the dict
TRANSITIONS_PUBLISHER = dict(TRANSITIONS_PUBLISHER)
