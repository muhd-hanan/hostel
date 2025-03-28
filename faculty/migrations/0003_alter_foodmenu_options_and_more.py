# Generated by Django 5.1.4 on 2025-03-25 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0002_alter_washslot_options_remove_washslot_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodmenu',
            options={'ordering': ['meal_type'], 'verbose_name': 'food menu', 'verbose_name_plural': 'food menus'},
        ),
        migrations.AlterUniqueTogether(
            name='foodmenu',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='foodmenu',
            name='day',
            field=models.CharField(choices=[('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')], default='sunday', max_length=9),
        ),
        migrations.RemoveField(
            model_name='foodmenu',
            name='date',
        ),
    ]
