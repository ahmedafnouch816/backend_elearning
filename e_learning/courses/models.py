from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None  # On supprime le champ username par défaut d'AbstractUser

    class Role(models.TextChoices):
        STUDENT = 'student', 'Étudiant'
        TEACHER = 'teacher', 'Formateur'
        ADMIN = 'admin', 'Administrateur'

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Pas de champs obligatoires en plus

    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email



# Cours
class Cours(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    formateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cours')

    def __str__(self):
        return self.titre

# Séance
class Seance(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='seances')
    titre = models.CharField(max_length=255)
    date = models.DateTimeField()
    lien_reunion = models.URLField()
    video_enregistrement = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return self.titre

# Document
class Document(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='documents')
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.titre

# Notification (optionnel)
class Notification(models.Model):
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
