# Generated by Django 4.1.4 on 2023-01-16 18:30

from django.db import migrations, models
import hospital.models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_alter_user_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=hospital.models.f),
        ),
    ]