from uuid import uuid4

from rest_framework import serializers
from .models import QuestionnaireIntervention,Candidate, Intervention1, Intervention2, Intervention3, Intervention4
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

    ques_answer = serializers.SerializerMethodField()

    class Meta:
        model = Intervention1
        fields = "__all__"

    def get_ques_answer(self, obj):

        if not obj.ques_answer:
            return []

        updated_answers = []

        for item in obj.ques_answer:

            # item = [1, true]

            question_id = item[0]
            answer = item[1]

            question_text = ""

            question = QuestionnaireIntervention.objects.filter(
                id=question_id
            ).first()

            if question:
                question_text = question.question_text

            # return in this format:
            # [1, "question text", true]

            updated_answers.append([
                question_id,
                question_text,
                answer
            ])

        return updated_answers


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
        source="interventions1",
        many=True,
        read_only=True
    )

    intervention2 = Intervention2Serializer(
        source="interventions2",
        many=True,
        read_only=True
    )

    intervention3 = Intervention3Serializer(
        source="interventions3",
        many=True,
        read_only=True
    )

    intervention4 = Intervention4Serializer(
        source="interventions4",
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
  
  