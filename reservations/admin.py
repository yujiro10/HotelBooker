from django.contrib import admin

from .models import Chambre, ClientProfile, Reservation


@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = ("numero_chambre", "type_chambre", "prix_nuit")
    list_filter = ("type_chambre",)
    search_fields = ("numero_chambre",)


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "telephone")
    search_fields = ("user__username", "user__first_name", "user__last_name", "telephone")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("client", "chambre", "date_debut", "date_fin", "nombre_nuits_admin", "statut_admin")
    list_filter = ("chambre__type_chambre", "date_debut", "date_fin")
    search_fields = ("client__username", "client__first_name", "client__last_name", "chambre__numero_chambre")
    date_hierarchy = "date_debut"

    @admin.display(description="Nuits")
    def nombre_nuits_admin(self, obj: Reservation) -> int:
        return obj.nombre_nuits

    @admin.display(description="Statut")
    def statut_admin(self, obj: Reservation) -> str:
        return obj.statut
