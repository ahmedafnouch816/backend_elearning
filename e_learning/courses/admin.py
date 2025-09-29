from django.contrib import admin
from .models import User, Cours, Seance, Document, Notification

# Enregistrer le modèle User personnalisé
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)

admin.site.register(User, UserAdmin)

# Enregistrer le modèle Cours
class CoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'formateur', 'description')
    search_fields = ('titre', 'formateur__username')
    list_filter = ('formateur',)

admin.site.register(Cours, CoursAdmin)

# Enregistrer le modèle Seance
class SeanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'cours', 'date', 'lien_reunion')
    search_fields = ('titre', 'cours__titre')
    list_filter = ('cours',)

admin.site.register(Seance, SeanceAdmin)

# Enregistrer le modèle Document
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'seance', 'fichier')
    search_fields = ('titre', 'seance__titre')
    list_filter = ('seance',)

admin.site.register(Document, DocumentAdmin)

# Enregistrer le modèle Notification
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'destinataire', 'message', 'date_envoi')
    search_fields = ('destinataire__username', 'message')
    list_filter = ('destinataire',)

admin.site.register(Notification, NotificationAdmin)
