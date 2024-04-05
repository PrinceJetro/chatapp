from rest_framework.serializers import ModelSerializer
from .models import Complaint

class ComplaintSerializer(ModelSerializer):
    class Meta:
        model = Complaint
        fields ='__all__'
