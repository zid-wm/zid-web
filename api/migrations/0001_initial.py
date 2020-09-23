# Generated by Django 3.1.1 on 2020-09-13 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControllerSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callsign', models.CharField(max_length=16)),
                ('start', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controller_sessions', to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callsign', models.CharField(max_length=16)),
                ('frequency', models.DecimalField(decimal_places=3, max_digits=6)),
                ('online_since', models.DateTimeField()),
                ('last_update', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controller_online', to='user.user')),
            ],
        ),
    ]