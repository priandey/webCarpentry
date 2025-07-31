from io import BytesIO
import logging
import os

from django.utils.crypto import get_random_string
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files import File
from PIL import Image


class Chantier(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_of_work = models.DateField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def pictures_count(self):
        return len(self.pictures.all())

    @property
    def thumbnail(self):
        try:
            return self.pictures.filter(is_main=True)[0]
        except IndexError:
            return None


class Picture(models.Model):
    class Meta:
        verbose_name = "Image"

    chantier = models.ForeignKey(Chantier, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to='images/', verbose_name="Fichier")
    description = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    is_main = models.BooleanField(default=False, verbose_name="Image de couverture")

    def thumbnailify(self):
        logging.info("Creating thumbnail for %s", self.picture.name)
        try:
            # Open image and convert to RGB if necessary (handles PNG transparency)
            img = Image.open(self.picture)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            # Calculate aspect ratio preserving thumbnail
            # Original dimensions: 6000x300 seems unusual - let's use more standard sizes
            max_width, max_height = 800, 600

            # Calculate new dimensions preserving aspect ratio
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # Create thumbnail with optimized settings
            thumbnail_io = BytesIO()
            img.save(thumbnail_io, 'JPEG', quality=85, optimize=True)
            thumbnail_io.seek(0)

            # Generate filename with original extension
            original_name = self.picture.name.split('/')[-1]
            name, ext = os.path.splitext(original_name)
            thumbnail_name = f"{name}_thumb{ext}"

            return File(thumbnail_io, name=f"thumbnails/{thumbnail_name}")

        except Exception as e:
            # Log error and return None to prevent save failure
            logging.error("Error creating thumbnail for %s: %s", self.picture.name, e)
            return None

    def save(self, *args, **kwargs):
        self.thumbnail = self.thumbnailify()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)


@receiver(post_delete, sender=Picture)
def submission_delete(sender, instance, **kwargs):
    instance.picture.delete(False)
