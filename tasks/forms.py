from django import forms
from django.core.exceptions import ValidationError
from . import models
import datetime
from users.models import CustomUser


class DateInput(forms.DateInput):
    input_type = 'date'


class AddTaskForm(forms.ModelForm):
    title = forms.CharField(
        label='Task Title',
        widget=forms.TextInput(attrs={
            'name': 'title',
            'placeholder': 'Task Title',
        })
    )

    description = forms.CharField(
        label='Task Description',
        widget=forms.TextInput(attrs={
            'name': 'description',
            'placeholder': 'Task Description',
        })
    )

    date = forms.DateField(
        label='Date',
        widget=DateInput(attrs={
            'name': 'date',
            'placeholder': 'Date',
        })
    )

    class Meta:
        model = models.Task
        fields = ('title', 'description', 'date')

    def clean_date(self):
        date = self.cleaned_data.get('date')

        if date < datetime.date.today():
            raise ValidationError(f'You cannot input date from the past')

        return date
