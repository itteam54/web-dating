# Generated by Django 4.2.1 on 2023-05-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0007_alter_profile_body_type_alter_profile_children_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="children",
            field=models.BooleanField(default=False),
        ),
    ]
