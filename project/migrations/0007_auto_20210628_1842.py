# Generated by Django 3.2.4 on 2021-06-28 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_alter_appointment_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='pesel',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profil',
            name='phone',
            field=models.SmallIntegerField(null=True),
        ),
    ]