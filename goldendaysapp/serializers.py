from uuid import uuid4

from rest_framework import serializers
from .models import QuestionnaireIntervention,Candidate, Intervention1, Intervention2, Intervention3, Intervention4,AllLog
from .models import (
    District,
    Almora,
    Bageshwar,
    Chamoli,
    Champawat,
    Dehradun,
    Haridwar,
    Nanital,
    Pauri,
    Pithoragarh,
    Rudraprayag,
    Tehri,
    Usnagar,
    Uttarkashi,SectorLogin
)
DISTRICT_MODEL_MAP = {
    "almora": Almora,
    "bageshwar": Bageshwar,
    "chamoli": Chamoli,
    "champawat": Champawat,
    "dehradun": Dehradun,
    "haridwar": Haridwar,
    "nanital": Nanital,
    "pauri": Pauri,
    "pithoragarh": Pithoragarh,
    "rudraprayag": Rudraprayag,
    "tehri": Tehri,
    "usnagar": Usnagar,
    "uttarkashi": Uttarkashi,
}


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

    


class Intervention1Serializer(serializers.ModelSerializer):

    class Meta:
        model = Intervention1
        fields = "__all__"

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if not instance.ques_answer:
            data["ques_answer"] = []
            return data

        updated_answers = []

        for item in instance.ques_answer:

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

        data["ques_answer"] = updated_answers

        return data


class Intervention2Serializer(serializers.ModelSerializer):

    class Meta:
        model = Intervention2
        fields = "__all__"

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if not instance.ques_answer:
            data["ques_answer"] = []
            return data

        updated_answers = []

        for item in instance.ques_answer:

            question_id = item[0]
            answer = item[1]

            question_text = ""

            question = QuestionnaireIntervention.objects.filter(
                id=question_id
            ).first()

            if question:
                question_text = question.question_text

            updated_answers.append([
                question_id,
                question_text,
                answer
            ])

        data["ques_answer"] = updated_answers

        return data

class Intervention3Serializer(serializers.ModelSerializer):

    class Meta:
        model = Intervention3
        fields = "__all__"

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if not instance.ques_answer:
            data["ques_answer"] = []
            return data

        updated_answers = []

        for item in instance.ques_answer:

            # item = [1, true]

            question_id = item[0]
            answer = item[1]

            question_text = ""

            question = QuestionnaireIntervention.objects.filter(
                id=question_id
            ).first()

            if question:
                question_text = question.question_text

            updated_answers.append([
                question_id,
                question_text,
                answer
            ])

        data["ques_answer"] = updated_answers

        return data

class Intervention4Serializer(serializers.ModelSerializer):

    class Meta:
        model = Intervention4
        fields = "__all__"

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if not instance.ques_answer:
            data["ques_answer"] = []
            return data

        updated_answers = []

        for item in instance.ques_answer:

            # item = [1, true]

            question_id = item[0]
            answer = item[1]

            question_text = ""

            question = QuestionnaireIntervention.objects.filter(
                id=question_id
            ).first()

            if question:
                question_text = question.question_text

            updated_answers.append([
                question_id,
                question_text,
                answer
            ])

        data["ques_answer"] = updated_answers

        return data


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

    district = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()
    awc_name = serializers.SerializerMethodField()
    sector_id = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = "__all__"

    # =====================================
    # Get AWC Details
    # =====================================

    def get_awc_data(self, obj):

        try:

            user = obj.registered_by

            if not user:
                return None

            username = user.username

        except AllLog.DoesNotExist:
            return None

        # Search all district tables
        for district_name, model in DISTRICT_MODEL_MAP.items():

            awc = model.objects.filter(
                awc_code=username
            ).first()

            if awc:

                # =====================================
                # Get Supervisor Unique ID
                # =====================================

                supervisor = AllLog.objects.filter(
                    username=awc.sector,
                    role="supervisor"
                ).first()

                return {
                    "district": district_name,
                    "project": awc.project,
                    "sector": awc.sector,
                    "awc_name": awc.awc,
                    "sector_id": supervisor.unique_id if supervisor else None
                }

        return None

    def get_district(self, obj):

        data = self.get_awc_data(obj)

        return data["district"] if data else None

    def get_project(self, obj):

        data = self.get_awc_data(obj)

        return data["project"] if data else None

    def get_sector(self, obj):

        data = self.get_awc_data(obj)

        return data["sector"] if data else None

    def get_awc_name(self, obj):

        data = self.get_awc_data(obj)

        return data["awc_name"] if data else None

    def get_sector_id(self, obj):

        data = self.get_awc_data(obj)

        return data["sector_id"] if data else None
      
  
class QuestionnaireInterventionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionnaireIntervention
        fields = "__all__"
  
  