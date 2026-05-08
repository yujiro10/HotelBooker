from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Chambre(models.Model):
    TYPE_CHOICES = [
        ("simple", "Simple"),
        ("double", "Double"),
        ("suite", "Suite"),
        ("luxe", "Luxe"),
    ]

    numero_chambre = models.CharField(max_length=10, unique=True)
    type_chambre = models.CharField(max_length=10, choices=TYPE_CHOICES)
    prix_nuit = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["numero_chambre"]

    def __str__(self) -> str:
        return f"Chambre {self.numero_chambre} ({self.get_type_chambre_display()})"


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    telephone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username}"


class Reservation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    chambre = models.ForeignKey(Chambre, on_delete=models.PROTECT, related_name="reservations")
    date_debut = models.DateField()
    date_fin = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_debut"]

    def clean(self) -> None:
        if self.date_debut >= self.date_fin:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")

        conflits = Reservation.objects.filter(chambre=self.chambre).exclude(pk=self.pk).filter(
            date_debut__lt=self.date_fin, date_fin__gt=self.date_debut
        )
        if conflits.exists():
            raise ValidationError("Cette chambre est déjà réservée sur cette période.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def nombre_nuits(self) -> int:
        return (self.date_fin - self.date_debut).days

    @property
    def statut(self) -> str:
        today = timezone.localdate()
        if today < self.date_debut:
            return "Confirmée"
        if self.date_debut <= today < self.date_fin:
            return "En cours"
        return "Terminée"

    def __str__(self) -> str:
        return f"{self.client.username} - {self.chambre.numero_chambre} ({self.date_debut} -> {self.date_fin})"
