# Generated by Django 4.0.6 on 2022-07-25 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_remove_note_image_alter_note_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]
