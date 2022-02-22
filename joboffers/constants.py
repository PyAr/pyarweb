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
        'icon_class': 'glyphicon-arrow-up'
    },
    CODE_DEACTIVATE: {
        'target_url': 'joboffers:deactivate',
        'text': _('Desactivar'),
        'css_classes': ['btn-warning'],
        'icon_class': 'glyphicon-minus-sign'
    },
    CODE_REQUEST_MODERATION: {
        'target_url': 'joboffers:request_moderation',
        'text': _('Confirmar'),
        'css_classes': ['btn-success'],
        'icon_class': 'glyphicon-eye-open'
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
