from rest_framework import serializers
from ..models import Brand

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['title', 'slug']
