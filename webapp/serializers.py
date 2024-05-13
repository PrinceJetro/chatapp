from rest_framework.serializers import ModelSerializer
from .models import Complaint
from .models import OnlineClass

class ComplaintSerializer(ModelSerializer):
    class Meta:
        model = Complaint
        fields ='__all__'

class StudentSerializer(ModelSerializer):
    class Meta:
        model = OnlineClass
        fields ='__all__'
