from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chambre",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero_chambre", models.CharField(max_length=10, unique=True)),
                (
                    "type_chambre",
                    models.CharField(
                        choices=[("simple", "Simple"), ("double", "Double"), ("suite", "Suite"), ("luxe", "Luxe")],
                        max_length=10,
                    ),
                ),
                ("prix_nuit", models.DecimalField(decimal_places=2, max_digits=8)),
                ("description", models.TextField(blank=True)),
            ],
            options={"ordering": ["numero_chambre"]},
        ),
        migrations.CreateModel(
            name="ClientProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("telephone", models.CharField(blank=True, max_length=20)),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="client_profile", to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date_debut", models.DateField()),
                ("date_fin", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("chambre", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reservations", to="reservations.chambre")),
                ("client", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reservations", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-date_debut"]},
        ),
    ]
