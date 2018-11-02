from rest_framework import serializers

from recognition.models import Request


class RequestSerializer(serializers.ModelSerializer):
    """Serializer for requests"""

    class Meta:
        model = Request
        fields = (
            'description',
            'picture'
        )
