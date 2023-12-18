import os
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegistrationSerializer
from .models import User


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with email already exists")

        user = User(email=email, username=username)
        user.set_password(password)
        user.save()


        site_url = os.environ.get("CLIENT_API_URL")
        subject = 'Registration on CarrotChecklist Successful'
        message = f'Thanks for registering. Go to the application by following the link: {site_url}'
        from_email = settings.DEFAULT_FROM_EMAIL  # Используем настройки из settings.py
        to_email = email

        try:
            send_mail(subject, message, from_email, [to_email])
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            user.delete()
            return Response({"success": False, "error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
