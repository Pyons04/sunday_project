from dataclasses import fields
from importlib.metadata import files
from django import forms
from .models import Status, Ticket
from django.contrib.auth.forms import AuthenticationForm

class TicketCreateForm(forms.ModelForm):
  class Meta:
    model = Ticket
    fields = ('title', 'description','status')

  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

class TicketUpdateForm(forms.ModelForm):
  class Meta:
    model = Ticket
    fields = ('title', 'description','status', 'deadlinedate')

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

class LoginForm(AuthenticationForm):

    # bootstrap4対応
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる