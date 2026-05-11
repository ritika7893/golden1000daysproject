from django.shortcuts import render
from uuid import uuid4
# Create your views here.
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from django.db.models.functions import Lower
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.db.models import Q
from django.utils import timezone
from django.db.models import F, Window,Max
from django.db.models.functions import DenseRank
from django.db import transaction
from datetime import datetime
from django.db.models import Avg
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
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

from rest_framework.permissions import IsAuthenticated

from goldendaysapp.permissions import IsAnganwadi,IsDirector
from goldendaysapp.serializers import Intervention4Serializer,Intervention3Serializer,Intervention2Serializer,QuestionnaireInterventionSerializer,Intervention1Serializer,CandidateDetailSerializer, CandidateSerializer


from .models import CdpoLogin,Intervention4,Intervention3,Intervention2,Intervention1,AllLog,Candidate,QuestionnaireIntervention
class LoginAPIView(APIView):
    def post(self, request):

        email_or_phone = request.data.get("email_or_phone")
        username = request.data.get("username")   # Ã°Å¸â€˜Ë† changed
        password = request.data.get("password")
        role = request.data.get("role")

        if not password or not role:
            return Response(
                {"error": "Password and role are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            # ----------------------------
            # ADMIN LOGIN (EMAIL / PHONE)
            # ----------------------------
            if role == "admin":

                if not email_or_phone:
                    return Response(
                        {"error": "Email or phone required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if "@" in email_or_phone:
                    user = AllLog.objects.get(email=email_or_phone, role="admin")
                else:
                    user = AllLog.objects.get(phone=email_or_phone, role="admin")

            # ----------------------------
            # OTHER USERS LOGIN (USERNAME)
            # ----------------------------
            else:

                if not username:
                    return Response(
                        {"error": "Username is required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                user = AllLog.objects.get(username=username, role=role)

            # ----------------------------
            # CHECK ACTIVE
            # ----------------------------
            if not user.is_active:
                return Response(
                    {"error": "Account is disabled"},
                    status=status.HTTP_403_FORBIDDEN
                )
            if check_password("Test@1234", user.password):
                return Response(
                    {
                        "error": "Default password not allowed. Please reset your password.",
                        "action": "FORGOT_PASSWORD_REQUIRED"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            # ----------------------------
            # CHECK PASSWORD
            # ----------------------------
            if password != user.password:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # ----------------------------
            # JWT TOKEN
            # ----------------------------
            refresh = RefreshToken.for_user(user)
            refresh["role"] = user.role
            refresh["unique_id"] = user.unique_id

            return Response(
                {
                    "message": "Login successful",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": user.role,
                    "unique_id": user.unique_id,
                },
                status=status.HTTP_200_OK
            )

        except AllLog.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
class RefreshTokenAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            return Response(
                {
                    "access": str(access)
                },
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
class ResetPasswordAPIView(APIView):
    def post(self, request):

        username = request.data.get("username")   # ðŸ‘ˆ changed
        role = request.data.get("role")
        new_password = request.data.get("new_password")

        if not username or not role or not new_password:
            return Response(
                {"error": "username, role and new_password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = AllLog.objects.get(username=username, role=role)  # ðŸ‘ˆ changed

            # âœ… optional safety check
            if not user.is_active:
                return Response(
                    {"error": "Account is disabled"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # âœ… update password
            user.password = make_password(new_password)
            user.save()

            return Response(
                {"message": "Password reset successful"},
                status=status.HTTP_200_OK
            )

        except AllLog.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class UserListAPIView(APIView):
    def get(self, request):
        users = AllLog.objects.all().values("username","unique_id","role")

        return Response(
            {
                "count": len(users),
                "data": list(users)
            },
            status=status.HTTP_200_OK
        )
        


class CandidateAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [
        IsAuthenticated
    ]
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAnganwadi()]  # no permissions for GET
        return [IsAuthenticated()] 
    # =========================
    # GET
    # =========================

    def get(self, request):

        candidate_id = request.query_params.get("candidate_id")

        if candidate_id:

            try:

                candidate = Candidate.objects.get(
                    candidate_id=candidate_id
                )

                serializer = CandidateSerializer(candidate)

                return Response(
                    {
                        "success": True,
                        "data": serializer.data
                    }
                )

            except Candidate.DoesNotExist:

                return Response(
                    {
                        "success": False,
                        "message": "Candidate not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        candidates = Candidate.objects.all().order_by("-created_at")

        serializer = CandidateSerializer(
            candidates,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )


    def post(self, request):
    
        serializer = CandidateSerializer(
            data=request.data
        )
    
        if serializer.is_valid():
    
            user_log = AllLog.objects.filter(
                unique_id=request.user.unique_id
            ).first()
    
            if not user_log:
    
                return Response(
                    {
                        "success": False,
                        "message": "Authenticated user not found in AllLog"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
    
            candidate = serializer.save(
             
                registered_by=user_log
            )
    
            return Response(
                {
                    "success": True,
                    "message": "Candidate created successfully"
                },
                status=status.HTTP_201_CREATED
            )
    
        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request):

        candidate_id = request.data.get("candidate_id")

        if not candidate_id:

            return Response(
                {
                    "success": False,
                    "message": "candidate_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            candidate = Candidate.objects.get(
                candidate_id=candidate_id
            )

        except Candidate.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Candidate not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CandidateSerializer(
            candidate,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

           

            updated_candidate = serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Candidate updated successfully",
                    "data": CandidateSerializer(updated_candidate).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # =========================
    # DELETE
    # =========================

    def delete(self, request):

        candidate_id = request.data.get("candidate_id")

        if not candidate_id:

            return Response(
                {
                    "success": False,
                    "message": "candidate_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            candidate = Candidate.objects.get(
                candidate_id=candidate_id
            )

        except Candidate.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Candidate not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        candidate.delete()

        return Response(
            {
                "success": True,
                "message": "Candidate deleted successfully"
            },
            status=status.HTTP_200_OK
        )
    
class CandidateDetailAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):

        candidate_id = request.query_params.get("candidate_id")

        registered_by = request.query_params.get("registered_by")

        candidates = Candidate.objects.all()

        if candidate_id:

            candidates = candidates.filter(
                candidate_id=candidate_id
            )

        if registered_by:

            candidates = candidates.filter(
                registered_by=registered_by
            )

        if not candidates.exists():

            return Response(
                {
                    "success": False,
                    "message": "Candidate not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if candidate_id and candidates.count() == 1:

            serializer = CandidateDetailSerializer(
                candidates.first()
            )

        else:

            serializer = CandidateDetailSerializer(
                candidates,
                many=True
            )

        return Response(
            {
                "success": True,
                "count": candidates.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
        
class Intervention1CreateAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAnganwadi()]
        return [IsAuthenticated()]

    def post(self, request):

        serializer = Intervention1Serializer(data=request.data)

        if serializer.is_valid():

            candidate_id = serializer.validated_data.get("candidate_id")

            # Check candidate exists
            if not candidate_id:
                return Response(
                    {
                        "success": False,
                        "message": "candidate_id is required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            already_exists = Intervention1.objects.filter(candidate_id=candidate_id).exists()
    
            if already_exists:
                return Response(
                    {
                        "success": False,
                        "message": (
                            "Intervention already exists for this candidate. "
                            "One candidate can have only one intervention."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_log = AllLog.objects.filter(
                unique_id=request.user.unique_id
            ).first()

            if not user_log:
                return Response(
                    {
                        "success": False,
                        "message": "Authenticated user not found in AllLog"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            intervention = serializer.save(
                created_by=user_log
            )

            return Response(
                {
                    "success": True,
                    "message": "Intervention created successfully",
                    "data": Intervention1Serializer(intervention).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
class QuestionnaireInterventionAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsDirector()]
        return [IsAuthenticated()]

    # =========================
    # GET
    # =========================

    def get(self, request):

        questionnaire_id = request.query_params.get("id")

        if questionnaire_id:

            try:

                questionnaire = QuestionnaireIntervention.objects.get(
                    id=questionnaire_id
                )

                serializer = QuestionnaireInterventionSerializer(
                    questionnaire
                )

                return Response(
                    {
                        "success": True,
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            except QuestionnaireIntervention.DoesNotExist:

                return Response(
                    {
                        "success": False,
                        "message": "Questionnaire not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        questionnaires = QuestionnaireIntervention.objects.all().order_by(
            "-created_at"
        )

        serializer = QuestionnaireInterventionSerializer(
            questionnaires,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    # =========================
    # POST
    # =========================

    def post(self, request):

        serializer = QuestionnaireInterventionSerializer(
            data=request.data
        )

        if serializer.is_valid():

            questionnaire = serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Questionnaire created successfully",
                    "data": QuestionnaireInterventionSerializer(
                        questionnaire
                    ).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # =========================
    # PUT
    # =========================

    def put(self, request):

        questionnaire_id = request.data.get("id")

        if not questionnaire_id:

            return Response(
                {
                    "success": False,
                    "message": "id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            questionnaire = QuestionnaireIntervention.objects.get(
                id=questionnaire_id
            )

        except QuestionnaireIntervention.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Questionnaire not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = QuestionnaireInterventionSerializer(
            questionnaire,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_questionnaire = serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Questionnaire updated successfully",
                    "data": QuestionnaireInterventionSerializer(
                        updated_questionnaire
                    ).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # =========================
    # DELETE
    # =========================

    def delete(self, request):

        questionnaire_id = request.data.get("id")

        if not questionnaire_id:

            return Response(
                {
                    "success": False,
                    "message": "id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            questionnaire = QuestionnaireIntervention.objects.get(
                id=questionnaire_id
            )

        except QuestionnaireIntervention.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Questionnaire not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        questionnaire.delete()

        return Response(
            {
                "success": True,
                "message": "Questionnaire deleted successfully"
            },
            status=status.HTTP_200_OK
        )
        
class Intervention2CreateAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAnganwadi()]
        return [IsAuthenticated()]

    def post(self, request):

        serializer = Intervention2Serializer(data=request.data)

        if serializer.is_valid():

            candidate_id = serializer.validated_data.get("candidate_id")

            # Check candidate exists
            if not candidate_id:
                return Response(
                    {
                        "success": False,
                        "message": "candidate_id is required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            already_exists = Intervention2.objects.filter(
                candidate_id=candidate_id
            ).exists()

            if already_exists:
                return Response(
                    {
                        "success": False,
                        "message": (
                            "Intervention already exists for this candidate. "
                            "One candidate can have only one intervention."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_log = AllLog.objects.filter(
                unique_id=request.user.unique_id
            ).first()

            if not user_log:
                return Response(
                    {
                        "success": False,
                        "message": "Authenticated user not found in AllLog"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            intervention = serializer.save(
                created_by=user_log
            )

            return Response(
                {
                    "success": True,
                    "message": "Intervention2 created successfully",
                    "data": Intervention2Serializer(intervention).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
class Intervention3CreateAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):

        if self.request.method == "POST":
            return [IsAnganwadi()]

        return [IsAuthenticated()]

    def post(self, request):

        serializer = Intervention3Serializer(data=request.data)

        if serializer.is_valid():

            candidate_id = serializer.validated_data.get("candidate_id")

            # Check candidate exists
            if not candidate_id:
                return Response(
                    {
                        "success": False,
                        "message": "candidate_id is required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            already_exists = Intervention3.objects.filter(
                candidate_id=candidate_id
            ).exists()

            if already_exists:
                return Response(
                    {
                        "success": False,
                        "message": (
                            "Intervention already exists for this candidate. "
                            "One candidate can have only one intervention."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_log = AllLog.objects.filter(
                unique_id=request.user.unique_id
            ).first()

            if not user_log:
                return Response(
                    {
                        "success": False,
                        "message": "Authenticated user not found in AllLog"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            intervention = serializer.save(
                created_by=user_log
            )

            return Response(
                {
                    "success": True,
                    "message": "Intervention3 created successfully",
                    "data": Intervention3Serializer(intervention).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
class Intervention4CreateAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):

        if self.request.method == "POST":
            return [IsAnganwadi()]

        return [IsAuthenticated()]

    def post(self, request):

        serializer = Intervention4Serializer(data=request.data)

        if serializer.is_valid():

            candidate_id = serializer.validated_data.get("candidate_id")

            # Check candidate exists
            if not candidate_id:
                return Response(
                    {
                        "success": False,
                        "message": "candidate_id is required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            already_exists = Intervention4.objects.filter(
                candidate_id=candidate_id
            ).exists()

            if already_exists:
                return Response(
                    {
                        "success": False,
                        "message": (
                            "Intervention already exists for this candidate. "
                            "One candidate can have only one intervention."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_log = AllLog.objects.filter(
                unique_id=request.user.unique_id
            ).first()

            if not user_log:
                return Response(
                    {
                        "success": False,
                        "message": "Authenticated user not found in AllLog"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            intervention = serializer.save(
                created_by=user_log
            )

            return Response(
                {
                    "success": True,
                    "message": "Intervention4 created successfully",
                    "data": Intervention4Serializer(intervention).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
# views.py



# =========================
# Dynamic Model Mapping
# =========================

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


class AnganwadiDropdownAPIView(APIView):

    def get(self, request):

        district_name = request.GET.get("district")
        project = request.GET.get("project")
        sector = request.GET.get("sector")

        # =========================
        # 1. District List
        # =========================

        if not district_name:

            districts = District.objects.all().values(
                "district",
                "sdname"
            )

            data = [
                {
                  
                    "district": item["sdname"]
                }
                for item in districts
            ]

            return Response({
                "success": True,
                "type": "district",
                "data": data
            })

        # =========================
        # Get Dynamic Model
        # =========================

        model = DISTRICT_MODEL_MAP.get(district_name.lower())

        if not model:
            return Response({
                "success": False,
                "message": "Invalid district"
            }, status=status.HTTP_400_BAD_REQUEST)

        # =========================
        # 2. Project List
        # =========================

        if district_name and not project:

            projects = (
                model.objects
                .values("project")
                .distinct()
                .order_by("project")
            )

            data = [
                {
                    "project": item["project"]
                }
                for item in projects
            ]

            return Response({
                "success": True,
                "type": "project",
                "district": district_name,
                "data": data
            })

        # =========================
        # 3. Sector List
        # =========================

        if district_name and project and not sector:

            sectors = (
                model.objects
                .filter(project=project)
                .values("sector")
                .distinct()
                .order_by("sector")
            )

            data = [
                {
                    "sector": item["sector"]
                }
                for item in sectors
            ]

            return Response({
                "success": True,
                "type": "sector",
                "district": district_name,
                "project": project,
                "data": data
            })

        # =========================
        # 4. Anganwadi List
        # =========================

        awcs = (
            model.objects
            .filter(
                project=project,
                sector=sector
            )
            .values(
                "id",
                "awc",
                "awc_code",
                "awc_hindi"
            )
            .order_by("awc")
        )

        data = [
            {
                "id": item["id"],
                "awc_name": item["awc"],
                "awc_code": item["awc_code"],
                "awc_hindi": item["awc_hindi"],
                "display_name": f'{item["awc"]} ({item["awc_code"]})'
            }
            for item in awcs
        ]

        return Response({
            "success": True,
            "type": "anganwadi",
            "district": district_name,
            "project": project,
            "sector": sector,
            "data": data
        })
        
        
class SectorDropdownAPIView(APIView):

    def get(self, request):

        district = request.GET.get("district")

        # =========================
        # 1. District List
        # =========================

        if not district:

            districts = (
                SectorLogin.objects
                .values("district")
                .distinct()
                .order_by("district")
            )

            data = [
                {
                    "district": item["district"]
                }
                for item in districts
            ]

            return Response({
                "success": True,
                "type": "district",
                "data": data
            })

        # =========================
        # 2. Project + Sector List
        # =========================
    
        records = (
            SectorLogin.objects
            .filter(district=district)
            .values(
                "project_code",
                "sector"
            )
            .order_by("project_code", "sector")
        )
        
        grouped_data = {}
        
        for item in records:
        
            project_code = item["project_code"]
        
            if project_code not in grouped_data:
        
                grouped_data[project_code] = {
                    "project_code": item["project_code"],
                    "sectors": []
                }
        
            grouped_data[project_code]["sectors"].append({
                "sector": item["sector"]
            })
        
        return Response({
            "success": True,
            "type": "project_sector",
            "district": district,
            "data": list(grouped_data.values())
        })
class CdpoDropdownAPIView(APIView):

    def get(self, request):

        district = request.GET.get("district")

        # =========================
        # 1. District List
        # =========================

        if not district:

            districts = (
                CdpoLogin.objects
                .values("district")
                .distinct()
                .order_by("district")
            )

            data = [
                {
                    "district": item["district"]
                }
                for item in districts
            ]

            return Response({
                "success": True,
                "type": "district",
                "data": data
            })

        # =========================
        # 2. Project List
        # =========================

        projects = (
            CdpoLogin.objects
            .filter(district=district)
            .values("project_name")
            .distinct()
            .order_by("project_name")
        )

        data = [
            {
                "project_name": item["project_name"]
            }
            for item in projects
        ]

        return Response({
            "success": True,
            "type": "project",
            "district": district,
            "data": data
        })
class DistrictListAPIView(APIView):

    def get(self, request):

        districts = (
            District.objects
            .values(
                "sdname",
                "district"
            )
            .distinct()
            .order_by("sdname")
        )

        data = [
            {
                "sdname": item["sdname"],
                "district": item["district"]
            }
            for item in districts
        ]

        return Response({
            "success": True,
            "count": len(data),
            "data": data
        })