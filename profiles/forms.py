import autocomplete_light
from django import forms
from django.forms.models import inlineformset_factory
from cities_light.models import City
from .models import Profiles, ProfilesMediosContactos


class ProfileForm(forms.ModelForm):
    """
    Formulario para actualizar o crear tu perfil
    """
    ciudad = forms.ModelChoiceField(
         City.objects.all(), widget=autocomplete_light.ChoiceWidget('CityAutoComplete'))

    class Meta:
        model = Profiles
        exclude = ('user', )

# -- Inline form para medios de contacto de un perfil --
ProfilesMediosContactosFormSet = inlineformset_factory(Profiles,
                                                       ProfilesMediosContactos,
                                                       extra=1,
                                                       max_num=20,
                                                       can_delete=True)
