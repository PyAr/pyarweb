import autocomplete_light
from cities_light.models import City


class CityAutoComplete(autocomplete_light.AutocompleteModelBase):
    """
    Autocomplete de todas las ciudades.
    """
    search_fields = ['name', 'alternate_names']

autocomplete_light.register(City, CityAutoComplete)
