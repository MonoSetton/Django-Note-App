# Generated by Django 4.0.6 on 2022-07-25 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_note_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='image',
        ),
    ]