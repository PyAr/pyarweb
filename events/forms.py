# -*- coding: utf-8 -*-

from django import forms

from bootstrap3_datetime.widgets import DateTimePicker

from .models import Event


class EventForm(forms.ModelForm):
    start_at = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                "format": "DD/MM/YYYY HH:mm",
                "pickTime": True,
            }
        )
    )

    end_at = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                "format": "DD/MM/YYYY HH:mm",
                "pickTime": True
            }
        )
    )

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
