# Generated by Django 5.1 on 2024-09-03 10:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ratings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="teacher_images/"),
        ),
    ]
