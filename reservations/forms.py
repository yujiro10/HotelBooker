from django import forms

from .models import Chambre, Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["chambre", "date_debut", "date_fin"]
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "date_fin": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "chambre": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")
        chambre = cleaned_data.get("chambre")

        if not all([date_debut, date_fin, chambre]):
            return cleaned_data

        if date_debut >= date_fin:
            raise forms.ValidationError("La date de fin doit être postérieure à la date de début.")

        conflits = chambre.reservations.filter(date_debut__lt=date_fin, date_fin__gt=date_debut)
        if self.instance.pk:
            conflits = conflits.exclude(pk=self.instance.pk)
        if conflits.exists():
            raise forms.ValidationError("Cette chambre n'est pas disponible pour ces dates.")

        return cleaned_data


class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        fields = "__all__"
