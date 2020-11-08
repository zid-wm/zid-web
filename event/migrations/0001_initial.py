# Generated by Django 3.1 on 2020-11-07 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_auto_20200913_2343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('banner', models.URLField(null=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('host', models.CharField(max_length=16)),
                ('description', models.TextField(blank=True, null=True)),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EventPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callsign', models.CharField(max_length=16)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='event.event')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_positions', to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='EventSignup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signups', to='event.eventposition')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_signups', to='user.user')),
            ],
        ),
    ]
