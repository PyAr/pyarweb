from dataclasses import dataclass
from typing import Set

from pycompanies.models import UserCompanyProfile
from .models import OfferState
from .constants import (
    CODE_CREATE, CODE_EDIT, CODE_HISTORY, CODE_REJECT, CODE_REACTIVATE, CODE_DEACTIVATE,
    CODE_REQUEST_MODERATION, CODE_APPROVE
)

ACTIONS_PUBLISHER = {}
ACTIONS_ADMIN = {}

ROLE_PUBLISHER = "publisher"
ROLE_ADMIN = "admin"


@dataclass
class Action:
    verbose_name: str
    code: str
    valid_prev_states: tuple


def register_action(action: Action, role):
    """
    Populates the actions structure with the given action and role.
    The actions structure contains the actions allowed for every role
    for every joboffer state.
    """
    for state in action.valid_prev_states:
        if role == ROLE_PUBLISHER:
            ACTIONS_PUBLISHER[state].add(action.code)
        else:
            ACTIONS_ADMIN[state].add(action.code)


# Actions #


for state in OfferState.values:
    ACTIONS_PUBLISHER[state] = set()
    ACTIONS_ADMIN[state] = set()


create = Action(
    verbose_name="Crear",
    code=CODE_CREATE,
    valid_prev_states=(OfferState.NEW,)
)

edit = Action(
    verbose_name="Editar",
    code=CODE_EDIT,
    valid_prev_states=(
        OfferState.DEACTIVATED, OfferState.REJECTED, OfferState.EXPIRED
    ),
)

reject = Action(
    verbose_name="Rechazar",
    code=CODE_REJECT,
    valid_prev_states=(OfferState.MODERATION,),
)

reactivate = Action(
    verbose_name="Reactivar",
    code=CODE_REACTIVATE,
    valid_prev_states=(OfferState.EXPIRED,),
)

deactivate = Action(
    verbose_name="Desactivar",
    code=CODE_DEACTIVATE,
    valid_prev_states=(OfferState.EXPIRED, OfferState.ACTIVE),
)

request_moderation = Action(
    verbose_name="Enviar a moderación",
    code=CODE_REQUEST_MODERATION,
    valid_prev_states=(OfferState.DEACTIVATED,),
)

approve = Action(
    verbose_name="Aprobar",
    code=CODE_APPROVE,
    valid_prev_states=(OfferState.MODERATION,),
)

get_history = Action(
    verbose_name="Historial",
    code=CODE_HISTORY,
    valid_prev_states=(
        OfferState.MODERATION,
        OfferState.DEACTIVATED,
        OfferState.MODERATION,
        OfferState.ACTIVE,
        OfferState.EXPIRED,
        OfferState.REJECTED
    ),
)

# end actions #

register_action(create, ROLE_PUBLISHER)
register_action(edit, ROLE_PUBLISHER)
register_action(deactivate, ROLE_PUBLISHER)
register_action(reactivate, ROLE_PUBLISHER)
register_action(request_moderation, ROLE_PUBLISHER)
register_action(get_history, ROLE_PUBLISHER)

register_action(reject, ROLE_ADMIN)
register_action(approve, ROLE_ADMIN)
register_action(get_history, ROLE_ADMIN)


ACTIONS = {
    ROLE_PUBLISHER: ACTIONS_PUBLISHER,
    ROLE_ADMIN: ACTIONS_ADMIN
}


def _get_roles(company, user):
    """
    Retrieves a list of the roles marching the giben user and company
    """
    roles = set()

    if user.is_anonymous:
        return roles

    if user.is_superuser:
        roles.add(ROLE_ADMIN)

    company_profile_qs = UserCompanyProfile.objects.filter(company=company, user=user)

    if company_profile_qs.exists():
        roles.add(ROLE_PUBLISHER)

    return roles


def get_valid_actions(user, company, offer_state: OfferState, roles=None):
    """
    Return a list of valid actions for an user within a job
    """

    if roles is None:
        roles_ = _get_roles(company, user)
    else:
        roles_ = roles

    actions: Set[str] = set()

    for role in roles_:
        # Appends the actions for every role
        actions = actions | ACTIONS[role][offer_state]

    return actions
