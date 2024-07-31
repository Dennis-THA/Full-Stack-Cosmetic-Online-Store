# Generated by Django 5.0.7 on 2024-07-30 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("permalink", models.URLField()),
                ("thumbnail_url", models.ImageField(upload_to="thumbnails/")),
                ("hover_thumbnail_url", models.ImageField(upload_to="thumbnails/")),
                ("discount", models.CharField(blank=True, max_length=20)),
                ("before_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("current_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
