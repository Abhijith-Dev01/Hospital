# Generated by Django 3.2 on 2024-08-16 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_doctor_doctor_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='email',
            field=models.EmailField(default='ajayj3337@gmail.com', max_length=254),
            preserve_default=False,
        ),
    ]
