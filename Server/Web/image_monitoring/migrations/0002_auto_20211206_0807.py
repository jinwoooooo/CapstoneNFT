# Generated by Django 2.2.12 on 2021-12-06 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_monitoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uploadedFile',
            field=models.ImageField(upload_to='Uploaded_Files/'),
        ),
    ]
