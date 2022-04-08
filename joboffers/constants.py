from django.utils.translation import gettext as _

ADD_URL = 'joboffers:add'
ADMIN_URL = 'joboffers:admin'
VIEW_URL = 'joboffers:view'
LIST_URL = 'joboffers:list'
APPROVE_URL = 'joboffers:approve'
DEACTIVATE_URL = 'joboffers:deactivate'
VIEW_URL = 'joboffers:view'
REJECT_URL = 'joboffers:reject'
REQUEST_MODERATION_URL = 'joboffers:request_moderation'
HISTORY_URL = 'joboffers:history'
TRACK_CONTACT_INFO_URL = 'joboffers:track-contact-info-view'
ANALYTICS_URL = 'joboffers:analytics'
ANALYTICS_CSV_URL = 'joboffers:download-analytics-csv'

CODE_ANALYTICS = 'analytics'
CODE_CREATE = "create"
CODE_EDIT = "edit"
CODE_HISTORY = "history"
CODE_REJECT = "reject"
CODE_REACTIVATE = "reactivate"
CODE_DEACTIVATE = "deactivate"
CODE_REQUEST_MODERATION = "reqmod"
CODE_APPROVE = "approve"
CODE_ANALYTICS = 'analytics'


ACTION_BUTTONS = {
    CODE_ANALYTICS: {
      'target_url': 'joboffers:analytics',
      'text': _('Visualizaciones'),
      'css_classes': ['btn-dark-green'],
      'icon_class': 'glyphicon-eye-open',
      'title': _('Ver las estadísticas de visualizaciones de la oferta.')
    },
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
