# Generated by Django 5.1.4 on 2025-03-24 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_fee_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fee',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='fee',
            name='paid_amount',
            field=models.FloatField(default=0),
        ),
    ]
