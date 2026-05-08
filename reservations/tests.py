from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Chambre, Reservation


class ReservationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="client1", password="test12345")
        self.chambre = Chambre.objects.create(
            numero_chambre="101",
            type_chambre="simple",
            prix_nuit=90,
        )

    def test_reject_overlapping_reservations(self):
        today = timezone.localdate()
        Reservation.objects.create(
            client=self.user,
            chambre=self.chambre,
            date_debut=today + timedelta(days=1),
            date_fin=today + timedelta(days=4),
        )
        other = Reservation(
            client=self.user,
            chambre=self.chambre,
            date_debut=today + timedelta(days=3),
            date_fin=today + timedelta(days=5),
        )

        with self.assertRaises(ValidationError):
            other.full_clean()

    def test_nuits_and_statut(self):
        today = timezone.localdate()
        reservation = Reservation.objects.create(
            client=self.user,
            chambre=self.chambre,
            date_debut=today - timedelta(days=1),
            date_fin=today + timedelta(days=2),
        )

        self.assertEqual(reservation.nombre_nuits, 3)
        self.assertEqual(reservation.statut, "En cours")
