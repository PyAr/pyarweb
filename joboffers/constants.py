from django.utils.translation import gettext as _

CODE_CREATE = "create"
CODE_EDIT = "edit"
CODE_HISTORY = "history"
CODE_REJECT = "reject"
CODE_REACTIVATE = "reactivate"
CODE_DEACTIVATE = "deactivate"
CODE_REQUEST_MODERATION = "reqmod"
CODE_APPROVE = "approve"


ACTION_BUTTONS = {
    CODE_HISTORY: {
        'target_url': 'joboffers:history',
        'text': _('Historial'),
        'css_classes': ['btn-info'],
        'icon_class': 'glyphicon-time'
    },
    CODE_EDIT: {
        'target_url': 'joboffers:edit',
        'text': _('Editar'),
        'css_classes': ['btn-default'],
        'icon_class': 'glyphicon-pencil'
    },
    CODE_REJECT: {
        'target_url': 'joboffers:reject',
        'text': _('Rechazar'),
        'css_classes': ['btn-danger'],
        'icon_class': 'glyphicon-thumbs-down'
    },
    CODE_REACTIVATE: {
        'target_url': 'joboffers:reactivate',
        'text': _('Volver a Activar'),
        'css_classes': ['btn-default'],
        'icon_class': 'glyphicon-arrow-up',
        'title': _('No es necesaria la moderación, se activa directamente.')
    },
    CODE_DEACTIVATE: {
        'target_url': 'joboffers:deactivate',
        'text': _('Desactivar'),
        'css_classes': ['btn-warning'],
        'icon_class': 'glyphicon-minus-sign',
        'title': _(
          'Si la oferta está activa es necesario desactivar la oferta para poder editarla'
        )
    },
    CODE_REQUEST_MODERATION: {
        'target_url': 'joboffers:request_moderation',
        'text': _('Confirmar'),
        'css_classes': ['btn-success'],
        'icon_class': 'glyphicon-eye-open',
        'title': _('Al confirmar la oferta se enviará a moderación para que sea revisada.')
    },
    CODE_APPROVE: {
        'target_url': 'joboffers:approve',
        'text': _('Aprobar'),
        'css_classes': ['btn-success'],
        'icon_class': 'glyphicon-pencil'
    }
}

STATE_LABEL_CLASSES = {
    'ACTIVE': 'label-success',
    'DEACTIVATED': 'label-danger',
    'EXPIRED': 'label-warning',
    'MODERATION': 'label-primary',
    'NEW': 'label-info',
    'REJECTED': 'label-danger',
}

APPROVED_MAIL_SUBJECT = _('PyAr - Oferta de Trabajo Aprobada')
APPROVED_MAIL_BODY = _(
  'Le informamos que la oferta que envío a revisión (%(title)s) ha sido aprobada y ya se'
  ' encuentra listada en la página y fué replicada en las redes sociales.'
)
REJECTED_MAIL_SUBJECT = _('PyAr - Oferta de Trabajo Rechazada')
REJECTED_MAIL_BODY = _(
  'Le informamos que la oferta que envío a revisión (%(title)s) ha sido rechazada.\n'
  'Razón de Rechazo: %(reason)s \n'
  'Observación: %(text)s'
)
