from django.forms import ModelForm
from .models import *


class RoomForm(ModelForm):
    class Meta:
        model = Complaint
        fields = '__all__'
        exclude = ['host', 'participants', 'topic']

class AvatarForm(ModelForm):
    class Meta:
        model  = User
        fields =  ['avatar']