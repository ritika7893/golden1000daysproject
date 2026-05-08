from uuid import uuid4

from rest_framework import serializers
from .models import Candidate
class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = "__all__"
        read_only_fields = [
            "candidate_id"
        ]
        extra_kwargs = {
            "registered_by": {"required": False}
        }

    def validate(self, attrs):

        aadhar_number = attrs.get("aadhar_number")
        pregancy_num = attrs.get("pregancy_num")

        queryset = Candidate.objects.filter(
            aadhar_number=aadhar_number,
            pregancy_num=pregancy_num
        )

        # exclude current object during update
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "error":
                    "This Aadhaar number with same pregnancy number is already registered."
                }
            )

        return attrs

  