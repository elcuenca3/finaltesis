# Generated by Django 4.1.1 on 2022-10-08 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0011_alter_preguntasrespondidas_respuesta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntasrespondidas',
            name='respuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.elegirrespuesta'),
        ),
    ]