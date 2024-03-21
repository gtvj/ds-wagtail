from rest_framework import serializers


class RecordSerializer(serializers.CharField):
    """
    Serializer for RecordFields.
    """

    def to_representation(self, value):
        return {
            "iaid": value.iaid,
            "url": value.get_url(use_reference_number=False),
            "reference_number": value.reference_number,
        }
