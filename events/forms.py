# -*- coding: utf-8 -*-

from django import forms
from .models import Event

class EventForm(forms.ModelForm):
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