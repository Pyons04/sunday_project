from dataclasses import fields
from importlib.metadata import files
from django import forms
from .models import Status, Ticket

class TicketCreateForm(forms.ModelForm):
  class Meta:
    model = Ticket
    fields = ('title', 'description','status')

  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

class StatusCreateForm(forms.ModelForm):
  class Meta:
    model = Status
    fields = ('status', 'order')

  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'