# -*- coding: utf-8 -*-

from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    lat = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.HiddenInput()
    )
    lng = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Event
        fields = (
            'name',
            'description',
            'place',
            'address',
            'url',
            'start_at',
            'end_at'
        )

    def save(self, *args, **kwargs):
        super(EventForm, self).save(*args, **kwargs)
        self.instance.lat = self.cleaned_data.get('lat')
        self.instance.lng = self.cleaned_data.get('lng')
        self.instance.save()
