from rest_framework import serializers
from .models import Assessment, Note

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'
    
    def to_internal_value(self, data):
        data['processed_image'] = data['original_image']
        return super(serializers.ModelSerializer, self).to_internal_value(data)

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields = ['note']