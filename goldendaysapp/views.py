from django.shortcuts import render

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

from rest_framework.permissions import IsAuthenticated

from .serializers import StudentRegSerializer

from .models import AllLog, StudentReg
class LoginAPIView(APIView):
    def post(self, request):

        email_or_phone = request.data.get("email_or_phone")
        username = request.data.get("username")   # 👈 changed
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

            # ----------------------------
            # CHECK PASSWORD
            # ----------------------------
            if not check_password(password, user.password):
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