from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from pathlib import Path

from .forms import ReservationForm
from .models import Chambre, Reservation

PRICE_RANGES = [
    ("0-100", "0 - 100 EUR", 0, 100),
    ("101-150", "101 - 150 EUR", 101, 150),
    ("151-200", "151 - 200 EUR", 151, 200),
    ("201-300", "201 - 300 EUR", 201, 300),
    ("301+", "301+ EUR", 301, None),
]

ROOM_TYPE_CONTENT = {
    "simple": {
        "subtitle": "Confort essentiel",
        "features": ["1 lit simple", "Wi-Fi gratuit", "Salle de bain privee", "TV ecran plat"],
        "services": ["Menage quotidien", "Reception 24h/24", "Service reveil"],
    },
    "double": {
        "subtitle": "Confort a deux",
        "features": ["1 grand lit double", "Wi-Fi haut debit", "Climatisation", "Espace bureau"],
        "services": ["Petit-dejeuner en option", "Menage quotidien", "Assistance bagages"],
    },
    "suite": {
        "subtitle": "Espace et elegance",
        "features": ["Chambre + salon", "Lit king size", "Minibar", "Vue panoramique"],
        "services": ["Room service", "Check-in prioritaire", "Peignoir et chaussons"],
    },
    "luxe": {
        "subtitle": "Prestige et services premium",
        "features": ["Suite premium", "Lit king + salon prive", "Jacuzzi", "Terrasse privee"],
        "services": ["Conciergerie dediee", "Transfer aeroport", "Room service premium"],
    },
}

ROOM_IMAGE_SETS = {
    "simple": {
        "default": [
            "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1200&q=80",
        ],
        "cozy": [
            "https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1551776235-dde6d4829808?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1631049552057-403cdb8f0658?auto=format&fit=crop&w=1200&q=80",
        ],
        "business": [
            "https://images.unsplash.com/photo-1519710884006-9ee59e95de76?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1591088398332-8a7791972843?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    "double": {
        "default": [
            "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1598928636135-d146006ff4be?auto=format&fit=crop&w=1200&q=80",
        ],
        "family": [
            "https://images.unsplash.com/photo-1600585154205-5b9d275b2f69?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1568495248636-6432b97bd949?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?auto=format&fit=crop&w=1200&q=80",
        ],
        "romantic": [
            "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1616594039964-3f5b0f27287a?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    "suite": {
        "default": [
            "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1468824357306-a439d58ccb1c?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1595576508898-0ad5c879a061?auto=format&fit=crop&w=1200&q=80",
        ],
        "panoramic": [
            "https://images.unsplash.com/photo-1616486029423-aaa4789e8c9a?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80",
        ],
        "executive": [
            "https://images.unsplash.com/photo-1592229505726-ca121723b8ef?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1522798514-97ceb8c4f1c8?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1602002418082-dd4a2c6f5e6e?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    "luxe": {
        "default": [
            "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1455587734955-081b22074882?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?auto=format&fit=crop&w=1200&q=80",
        ],
        "jacuzzi": [
            "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?auto=format&fit=crop&w=1200&q=80",
        ],
        "terrace": [
            "https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1578898887337-a7e36d9f5f5b?auto=format&fit=crop&w=1200&q=80",
        ],
    },
}

ROOM_TYPE_LOCAL_DIR = {
    "simple": "chambre_simple",
    "double": "chambre_double",
    "suite": "suite",
    "luxe": "chambre_luxe",
}

ROOM_TYPE_CODED_IMAGES = {
    "simple": ["c1", "c2", "c3"],
    "double": ["c4", "c5", "c6"],
    "luxe": ["c8", "c9", "c10"],
    "suite": ["c12", "c13", "c14"],
}


def _local_room_type_photos(room_type: str) -> list[str]:
    folder_name = ROOM_TYPE_LOCAL_DIR.get(room_type)
    if not folder_name:
        return []
    folder = Path(settings.BASE_DIR) / "static" / folder_name
    if not folder.exists():
        return []

    local_images = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        local_images.extend(sorted(folder.glob(ext)))
    return [f"/static/{folder_name}/{img.name}" for img in local_images]


def _resolve_coded_images(room_type: str) -> list[str]:
    codes = ROOM_TYPE_CODED_IMAGES.get(room_type, [])
    if not codes:
        return []
    static_root = Path(settings.BASE_DIR) / "static"
    exts = (".jpg", ".jpeg", ".png", ".webp")
    urls: list[str] = []
    all_files = [p for p in static_root.rglob("*") if p.is_file()]
    for code in codes:
        found_path = None
        code_lower = code.lower()
        # Accept c1.jpg, c1 (1).jpg, C1_test.PNG, etc.
        for file_path in all_files:
            stem_lower = file_path.stem.lower().strip()
            suffix_lower = file_path.suffix.lower().strip()
            if suffix_lower not in exts:
                continue
            if stem_lower == code_lower or stem_lower.startswith(code_lower):
                found_path = file_path
                break
        if found_path:
            rel = found_path.relative_to(static_root).as_posix()
            urls.append(f"/static/{rel}")
    return urls


def room_photos_for_type(room_type: str, description: str = "", room_number: str = "") -> list[str]:
    # Priority: dedicated local photos for room 501 in static/chambre 501/
    if str(room_number) == "501":
        room_501_dir = Path(settings.BASE_DIR) / "static" / "chambre 501"
        local_images = []
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
            local_images.extend(sorted(room_501_dir.glob(ext)))
        if local_images:
            return [f"/static/chambre 501/{img.name}" for img in local_images[:3]]

    # Priority mapping requested by user: c1..c14 files.
    coded_images = _resolve_coded_images(room_type)
    if coded_images:
        return coded_images[:3] if len(coded_images) >= 3 else (coded_images * 3)[:3]

    # Then use local photos by room type if available.
    type_local_photos = _local_room_type_photos(room_type)
    if type_local_photos:
        return type_local_photos[:3] if len(type_local_photos) >= 3 else (type_local_photos * 3)[:3]

    room_sets = ROOM_IMAGE_SETS.get(room_type, ROOM_IMAGE_SETS["simple"])
    desc = (description or "").lower()
    selected_key = "default"

    if room_type == "simple":
        if any(k in desc for k in ["cosy", "cozy", "calme", "repos"]):
            selected_key = "cozy"
        elif any(k in desc for k in ["bureau", "travail", "business"]):
            selected_key = "business"
    elif room_type == "double":
        if any(k in desc for k in ["famille", "familiale", "enfant"]):
            selected_key = "family"
        elif any(k in desc for k in ["romantique", "couple"]):
            selected_key = "romantic"
    elif room_type == "suite":
        if any(k in desc for k in ["vue", "panoramique"]):
            selected_key = "panoramic"
        elif any(k in desc for k in ["executive", "affaires"]):
            selected_key = "executive"
    elif room_type == "luxe":
        if "jacuzzi" in desc:
            selected_key = "jacuzzi"
        elif any(k in desc for k in ["terrasse", "terrace"]):
            selected_key = "terrace"

    photos = room_sets.get(selected_key, room_sets["default"])
    if not photos:
        return room_sets["default"]

    # Deterministic variation per room to avoid showing same photos.
    seed = sum(ord(c) for c in str(room_number))
    start_idx = seed % len(photos)
    return [photos[(start_idx + i) % len(photos)] for i in range(len(photos))]

class ChambreListView(LoginRequiredMixin, ListView):
    model = Chambre
    template_name = "reservations/chambre_list.html"
    context_object_name = "chambres"

    def get_queryset(self):
        qs = Chambre.objects.all()
        type_chambre = self.request.GET.get("type", "").strip()
        selected_price_range = self.request.GET.get("price_range", "").strip()

        if type_chambre:
            qs = qs.filter(type_chambre__iexact=type_chambre)

        if selected_price_range:
            for key, _label, min_price, max_price in PRICE_RANGES:
                if key == selected_price_range:
                    # Some SQLite datasets may store decimal-like values with commas.
                    # Filter in Python to support both "80.00" and "80,00" formats safely.
                    matching_ids = []
                    for chambre in qs:
                        try:
                            price_value = float(str(chambre.prix_nuit).replace(",", "."))
                        except (TypeError, ValueError):
                            continue
                        if max_price is None:
                            if price_value >= min_price:
                                matching_ids.append(chambre.id)
                        else:
                            if min_price <= price_value <= max_price:
                                matching_ids.append(chambre.id)
                    qs = Chambre.objects.filter(id__in=matching_ids)
                    break
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for chambre in context["chambres"]:
            chambre.preview_photo = room_photos_for_type(
                chambre.type_chambre,
                chambre.description,
                chambre.numero_chambre,
            )[0]
        context["type_choices"] = Chambre.TYPE_CHOICES
        context["price_ranges"] = [(key, label) for key, label, _min, _max in PRICE_RANGES]
        context["selected_type"] = self.request.GET.get("type", "").strip()
        context["selected_price_range"] = self.request.GET.get("price_range", "").strip()
        return context


class HomeView(ListView):
    model = Chambre
    template_name = "reservations/home.html"
    context_object_name = "chambres"

    def get_queryset(self):
        return Chambre.objects.all()[:6]


class ChambreDetailView(LoginRequiredMixin, DetailView):
    model = Chambre
    template_name = "reservations/chambre_detail.html"
    context_object_name = "chambre"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_data = ROOM_TYPE_CONTENT.get(self.object.type_chambre, ROOM_TYPE_CONTENT["simple"])
        context["room_subtitle"] = room_data["subtitle"]
        context["room_features"] = room_data["features"]
        context["room_services"] = room_data["services"]
        context["room_photos"] = room_photos_for_type(
            self.object.type_chambre,
            self.object.description,
            self.object.numero_chambre,
        )
        return context


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservations/reservation_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        qs = Reservation.objects.select_related("client", "chambre")
        if self.request.user.is_staff:
            return qs
        return qs.filter(client=self.request.user)


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservations/reservation_form.html"
    success_url = reverse_lazy("reservation_list")

    def get_initial(self):
        initial = super().get_initial()
        chambre_id = self.request.GET.get("chambre")
        if chambre_id:
            try:
                initial["chambre"] = int(chambre_id)
            except ValueError:
                pass
        return initial

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = "reservations/reservation_detail.html"
    context_object_name = "reservation"

    def get_queryset(self):
        qs = Reservation.objects.select_related("client", "chambre")
        if self.request.user.is_staff:
            return qs
        return qs.filter(client=self.request.user)
