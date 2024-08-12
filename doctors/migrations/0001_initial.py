# Generated by Django 3.2 on 2024-08-09 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('department', '0001_initial'),
        ('hospital_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documnents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_certificate', models.FileField(upload_to='')),
                ('experience_certificate', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('documnents_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='doctors.documnents')),
                ('salary', models.FloatField()),
                ('specialization', models.CharField(max_length=255)),
                ('degree', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('experience_years', models.IntegerField(default=0)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_data.hospital')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('doctors.documnents',),
        ),
    ]
