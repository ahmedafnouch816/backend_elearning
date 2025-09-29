from contextvars import Token
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

#API REGISTER 
class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                # Générer JWT token
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "status": 200,
                        "message": "Inscription réussie.",
                        "data": {
                            "user": {
                                "id": user.id,
                                "email": user.email,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                                "phone": user.phone,
                                "role": user.role,
                            },
                            "tokens": {
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                            }
                        },
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {
                    "status": 400,
                    "message": "Erreur lors de l'inscription.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "status": 500,
                    "message": "Une erreur est survenue.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
        


#API LOGIN 
class LoginApiClient(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                password = serializer.validated_data["password"]

                # Vérifier si l'utilisateur existe
                if not User.objects.filter(email=email).exists():
                    return Response(
                        {
                            "status": 404,
                            "message": "Email non trouvé",
                            "data": {}
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Authentification
                user = authenticate(request, username=email, password=password)
                if user is None:
                    return Response(
                        {
                            "status": 400,
                            "message": "Email ou mot de passe invalide",
                            "data": {}
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Générer JWT token
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "status": 200,
                        "message": "Connexion réussie.",
                        "data": {
                            "user": {
                                "id": user.id,
                                "email": user.email,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                                "phone": user.phone,
                                "role": user.role,
                            },
                            "tokens": {
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                            }
                        }
                    },
                    status=status.HTTP_200_OK
                )

            # Données invalides
            return Response(
                {
                    "status": 400,
                    "message": "Données invalides",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {
                    "status": 500,
                    "message": "Une erreur est survenue",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )