from rest_framework import serializers
from .models import User, Cours, Seance, Document

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)  # création normale
        user.set_password(password)  # hash du mot de passe
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    
    


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'titre', 'fichier']

class SeanceSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Seance
        fields = ['id', 'titre', 'date', 'lien_reunion', 'video_enregistrement', 'documents']

class CoursSerializer(serializers.ModelSerializer):
    seances = SeanceSerializer(many=True, read_only=True)
    class Meta:
        model = Cours
        fields = ['id', 'titre', 'description', 'formateur', 'seances']




