# Generated by Django 3.2.9 on 2024-09-30 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0001_initial'),
        ('users', '0002_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='faculty.faculty'),
        ),
    ]
