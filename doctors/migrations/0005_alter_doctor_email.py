# Generated by Django 3.2 on 2024-08-16 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0004_doctor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
