# Generated by Django 4.2.1 on 2023-05-25 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0002_alter_profile_body_type_alter_profile_education_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="height",
            field=models.DecimalField(decimal_places=0, default=170, max_digits=10),
        ),
    ]
