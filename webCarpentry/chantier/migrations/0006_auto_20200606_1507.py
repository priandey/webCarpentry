# Generated by Django 2.1.7 on 2020-06-06 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chantier', '0005_picture_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chantier',
            name='main_picture',
        ),
        migrations.AddField(
            model_name='picture',
            name='is_main',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='picture',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
    ]