# Generated by Django 5.0.7 on 2024-07-30 14:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_item"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="before_price",
        ),
        migrations.RemoveField(
            model_name="item",
            name="current_price",
        ),
        migrations.RemoveField(
            model_name="item",
            name="discount",
        ),
        migrations.RemoveField(
            model_name="item",
            name="hover_thumbnail_url",
        ),
        migrations.RemoveField(
            model_name="item",
            name="name",
        ),
        migrations.RemoveField(
            model_name="item",
            name="permalink",
        ),
        migrations.RemoveField(
            model_name="item",
            name="thumbnail_url",
        ),
        migrations.AddField(
            model_name="item",
            name="discount_label",
            field=models.CharField(default="No Discount", max_length=20),
        ),
        migrations.AddField(
            model_name="item",
            name="image",
            field=models.ImageField(
                default="static/website/images/1.jpg", upload_to="item_images/"
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="image_hover",
            field=models.ImageField(
                default="static/website/images/2.jpg", upload_to="item_images/"
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="old_price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name="item",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name="item",
            name="title",
            field=models.CharField(default="Default Title", max_length=200),
        ),
    ]
