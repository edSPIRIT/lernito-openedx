from rest_framework import serializers


class LernitoWebhookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    family = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    courseIds = serializers.ListField(child=serializers.CharField(max_length=255))

    def validate(self, data):
        """
        Check that at least one of courseIds is provided
        """
        if not data.get("courseIds"):
            raise serializers.ValidationError("At least one courseId must be provided")
        return data
