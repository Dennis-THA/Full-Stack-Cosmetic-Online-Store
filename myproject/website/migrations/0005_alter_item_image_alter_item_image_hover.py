# Generated by Django 5.0.7 on 2024-07-30 14:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_alter_item_discount_label_alter_item_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="image",
            field=models.ImageField(upload_to="item_images"),
        ),
        migrations.AlterField(
            model_name="item",
            name="image_hover",
            field=models.ImageField(upload_to="item_images"),
        ),
    ]
