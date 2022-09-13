from rest_framework import serializers
from basicapp.models import Project

# * Serializing the model
# * it will also convert it into a json objects
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # These fields has been serialized.
        fields = '__all__'
    