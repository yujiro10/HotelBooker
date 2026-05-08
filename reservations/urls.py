from django.urls import path

from .views import ChambreDetailView, ChambreListView, HomeView, ReservationCreateView, ReservationDetailView, ReservationListView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("reservations/", ReservationListView.as_view(), name="reservation_list"),
    path("mes-reservations/", ReservationListView.as_view(), name="mes_reservations"),
    path("reservations/new/", ReservationCreateView.as_view(), name="reservation_create"),
    path("reservations/<int:pk>/", ReservationDetailView.as_view(), name="reservation_detail"),
    path("chambres/", ChambreListView.as_view(), name="chambre_list"),
    path("chambres/<int:pk>/", ChambreDetailView.as_view(), name="chambre_detail"),
]
