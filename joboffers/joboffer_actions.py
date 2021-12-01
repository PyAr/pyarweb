from collections import defaultdict
from functools import wraps

from .models import OfferState

ACTIONS_PUBLISHER = defaultdict(dict)
ACTIONS_ADMIN = defaultdict(dict)

PROFILE_PUBLISHER = 'publisher'
PROFILE_ADMIN = 'admin'

CODE_EDIT = 'edit'
CODE_REJECT = 'reject'
CODE_COMMENT = 'comment'
CODE_REACTIVATE = 'reactivate'
CODE_DEACTIVATE = 'deactivate'
CODE_REQUEST_MODERATION = 'reqmod'
CODE_APPROVE = 'approve'


def register_action(func, profile):
    for state in func.valid_prev_states:
        if profile == PROFILE_PUBLISHER:
            ACTIONS_PUBLISHER[state][func.code] = func
        else:
            ACTIONS_ADMIN[state][func.code] = func


def check_state(func):
    @wraps(func)
    def wrapped(job_offer):
        if job_offer.state not in func.valid_prev_states:
            raise ValueError("Inconsistent state")
        else:
            result = func(job_offer)
            return result

    return wrapped


# see how to redirect to a view or call a different function
@check_state
def edit(job_offer):
    ...
edit.verbose_name = "Editar"
edit.code = CODE_EDIT
edit.valid_prev_states = (OfferState.DEACTIVATED, OfferState.REJECTED, OfferState.EXPIRED)


@check_state
def reject(job_offer):
    ...
reject.verbose_name = "Rechazar"
reject.code = CODE_REJECT
reject.valid_prev_states = (OfferState.MODERATION,)

# Me parece que moderate no existe, es comment
#def moderate():
def comment(job_offer):
    ...
comment.verbose_name = "Comentar"
comment.code = CODE_COMMENT
comment.valid_prev_states = (OfferState.MODERATION,)


def reactivate(job_offer):
    ...
reactivate.verbose_name = "Reactivar"
reactivate.code = CODE_REACTIVATE
reactivate.valid_prev_states = (OfferState.EXPIRED,)


def deactivate(job_offer):
    ...
deactivate.verbose_name = "Desactivar"
deactivate.code = CODE_DEACTIVATE
deactivate.valid_prev_states = (OfferState.EXPIRED, OfferState.ACTIVE)


def request_moderation(job_offer):
    ...
request_moderation.verbose_name = "Enviar a moderación"
request_moderation.code = CODE_REQUEST_MODERATION
request_moderation.valid_prev_states = (OfferState.DEACTIVATED,)


def approve(job_offer):
    ...
approve.verbose_name = "Aprobar"
approve.code = CODE_APPROVE
approve.valid_prev_states = (OfferState.MODERATION,)

register_action(edit, PROFILE_PUBLISHER)
register_action(deactivate, PROFILE_PUBLISHER)
register_action(request_moderation, PROFILE_PUBLISHER)

#
#Tambien estaria bueno poder decorar con un log para poder guardar el historial
#

ACTIONS = {
    PROFILE_PUBLISHER: dict(ACTIONS_PUBLISHER),
    PROFILE_ADMIN: dict(ACTIONS_ADMIN),
}


def _get_user_profile(user):
    """Get profile from user."""
    return PROFILE_PUBLISHER


def _is_owner(job_offer, user):
    """Check ownership of a job offfer."""
    return True


def get_valid_actions(job_offer, user):
    """Return valid action for user."""
    profile = _get_user_profile(user)
    state = job_offer.state

    if profile == PROFILE_ADMIN:
        return ACTIONS_ADMIN[state]
    else:
        if _is_owner(job_offer, user):
            return ACTIONS_PUBLISHER[state]
        else:
            raise ValueError()
