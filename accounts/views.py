from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import SupervisorProfile
from .serializers import RegisterSerializer, UserStatusSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        if SupervisorProfile.objects.filter(username=username).exists():
            return Response(
                {"message": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        return Response(
            {
                "message": "Registration successful. Awaiting approval.",
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = SupervisorProfile.objects.get(username=username)
        except SupervisorProfile.DoesNotExist:
            return Response(
                {"message": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {"message": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        status_responses = {
            'PENDING':  (403, "Approval pending. Please wait."),
            'REJECTED': (403, "Access rejected. Contact admin."),
            'REVOKED':  (403, "Access revoked. Contact admin."),
        }
        if user.status in status_responses:
            code, message = status_responses[user.status]
            return Response({"message": message}, status=code)

        # APPROVED — issue tokens
        refresh = RefreshToken.for_user(user)
        user.last_connected = timezone.now()
        user.save(update_fields=['last_connected'])

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
            "assigned_patient_mode": user.assigned_patient_mode,
            "status": user.status,
        })


class StatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserStatusSerializer(request.user)
        return Response(serializer.data)


class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token_str = request.data.get('token')
        if not token_str:
            return Response({"is_valid": False, "reason": "No token provided."})

        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(token_str)
            user = auth.get_user(validated_token)
        except (TokenError, InvalidToken, Exception) as e:
            return Response({"is_valid": False, "reason": str(e)})

        if user.status != 'APPROVED':
            return Response({
                "is_valid": False,
                "reason": f"Account status is {user.status}.",
            })

        user.last_connected = timezone.now()
        user.save(update_fields=['last_connected'])

        return Response({
            "is_valid": True,
            "username": user.username,
            "status": user.status,
            "assigned_patient_mode": user.assigned_patient_mode,
        })
