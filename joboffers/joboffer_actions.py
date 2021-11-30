from collections import defaultdict
from functools import wraps

from .models import OfferState

# def check_ownership(joboffer, current_editor, permission_required):
# TRANSITIONS_PUBLISHER = defaultdict(dict)
#
# def check_state(valid_states, next_state):
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
# https://docs.djangoproject.com/es/2.2/_modules/django/contrib/auth/decorators/

ACTIONS_PUBLISHER = defaultdict(list)
ACTIONS_ADMIN = defaultdict(list)

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
        ACTIONS_PUBLISHER[state].append({func.code: func})


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


# To avoid any further magic on accessing the dict
ACTIONS_PUBLISHER = dict(ACTIONS_PUBLISHER)

#Cuando vaya a una vista para saber que tengo que mostrar o
#que acciones tengo disponibles, por ejemplo, llamo al slug
#y me dice que acciones puedo hacer con la oferta, por ejemplo
#e aparece el boton editar. Tambien según el estado deberia
#mostrar algun que otro campo mas, pero esto deberia estar configurado
#en la vista o el template, pueden que sea mostrar o no cosas, directamente
#pasandole show_comment=True por ejemplo o show_cartel_rojo=False. Segun
#la vista en la que se este, y asi evitar tanta programacion en el template
#
#Una vez apretada la acción se manda a guardar, se podria apendear un mensaje
#al contexto y luego simplemente se recarga la pagina. Ver si conviene mandar el
#request a las transiciones para poder hacer esto o es ensuciar mucho
#
#Tambien estaria bueno poder decorar con un log para poder guardar el historial
#

ACTIONS = {
    PROFILE_PUBLISHER: dict(ACTIONS_PUBLISHER),
    PROFILE_ADMIN: dict(ACTIONS_ADMIN),
}
