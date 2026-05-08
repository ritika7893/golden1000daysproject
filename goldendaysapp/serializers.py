from uuid import uuid4

from rest_framework import serializers
from .models import Candidate, Intervention1, Intervention2, Intervention3, Intervention4, QuestionnaireIntervention
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


class Intervention1Serializer(serializers.ModelSerializer):

    class Meta:
        model = Intervention1
        fields = "__all__"


class Intervention2Serializer(serializers.ModelSerializer):

    class Meta:
        model = Intervention2
        fields = "__all__"


class Intervention3Serializer(serializers.ModelSerializer):

    class Meta:
        model = Intervention3
        fields = "__all__"


class Intervention4Serializer(serializers.ModelSerializer):

    class Meta:
        model = Intervention4
        fields = "__all__"


# =========================
# CANDIDATE DETAIL SERIALIZER
# =========================

class CandidateDetailSerializer(serializers.ModelSerializer):

    intervention1 = Intervention1Serializer(
        many=True,
        read_only=True
    )

    intervention2 = Intervention2Serializer(
        many=True,
        read_only=True
    )

    intervention3 = Intervention3Serializer(
        many=True,
        read_only=True
    )

    intervention4 = Intervention4Serializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Candidate

        fields = "__all__"

class QuestionnaireInterventionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionnaireIntervention
        fields = "__all__"
  
