# Generated by Django 5.1.6 on 2025-03-07 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_club_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opponent', models.CharField(max_length=100)),
                ('match_date', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('home_or_away', models.CharField(choices=[('Home', 'Home'), ('Away', 'Away')], max_length=10)),
                ('score', models.CharField(blank=True, max_length=10, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='users.club')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=50)),
                ('jersey_number', models.IntegerField(blank=True, null=True)),
                ('is_starting_xi', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='users.club')),
            ],
        ),
    ]
