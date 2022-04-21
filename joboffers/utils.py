import hashlib
import unicodedata
import plotly.graph_objects as go

from plotly.offline import plot

from django.db.models import Count
from django.utils.translation import gettext as _

from joboffers.models import EventType, JobOfferAccessLog

UNWANTED_SORROUNDING_CHARS = "@/#*"


def normalize(tag):
    """Normalize a single tag: remove non valid chars, lower case all."""
    tag_stripped = tag.strip()
    tag_stripped = tag_stripped.strip(UNWANTED_SORROUNDING_CHARS)
    value = unicodedata.normalize("NFKD", tag_stripped.lower())
    value = value.encode('ascii', 'ignore').decode('utf-8')
    return value


def normalize_tags(tags):
    """Parse a list of tags and removed duplicated tags and non valid chars."""
    return {normalize(tag) for tag in tags}


def hash_secret(credential: str):
    """Hash a secret string (so it can be logged safely.)"""
    if credential is not None:
        digest = hashlib.sha256(credential.encode('utf-8')).hexdigest()
    else:
        digest = 'None'

    return digest


def get_visualization_data(joboffer):
    """
    Retrieves a plain list of the visualizations for a joboffer
    """
    data = JobOfferAccessLog \
        .objects.filter(joboffer=joboffer) \
        .values_list('created_at', 'joboffer__id', 'joboffer__title', 'event_type')

    output_data = []

    for row in data:
        new_row = (*row, EventType(row[-1]).label)
        output_data.append(new_row)

    return output_data


def get_visualizations_graph(log_queryset):
    """
    Return a graph of the visualizations amount for the provided queryset.
    """
    if log_queryset.exists():
        grouping_qs = log_queryset\
          .order_by('created_at') \
          .values('created_at__date').annotate(Count('id'))

        dates = grouping_qs.values_list('created_at__date', flat=True)
        views_amount = grouping_qs.values_list('id__count', flat=True)

        fig = go.Figure(data=[go.Scatter(
          x=list(dates), y=list(views_amount)
        )])

        fig.update_layout(
          {"margin": {"l": 50, "r": 50, "b": 50, "t": 50, "pad": 4}}
        )

        fig.update_xaxes(
          dtick=1 * 1000 * 60 * 60 * 24,
          tickformat="%d-%m-%Y",
          tickangle=60
        )

        fig.update_yaxes(title=_("Visitas"), automargin=True)

        graph = plot(fig, output_type='div')
    else:
        graph = None

    return graph
