from .models import Messages, Conversations, Winks
from django import forms
from django.forms import Textarea

class MessageForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ('message_content', )

class WinkForm(forms.ModelForm):

    class Meta:
        model = Winks
        fields = ('sender', 'receiver', )
