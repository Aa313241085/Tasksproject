# Generated by Django 4.2.7 on 2024-02-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_user_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='client',
            field=models.CharField(choices=[('Yachdav', 'Yachdav'), ('Sky', 'Sky'), ('World Courier', 'World Courier'), ('Krief', 'Krief')], max_length=15),
        ),
    ]
