from io import BytesIO

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
        img = Image.open(self.picture)
        img.thumbnail((6000, 300))
        thumbnail_io = BytesIO()
        img.save(thumbnail_io, 'JPEG', quality=85)
        return File(thumbnail_io, name=get_random_string())

    def save(self, *args, **kwargs):
        self.thumbnail = self.thumbnailify()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

@receiver(post_delete, sender=Picture)
def submission_delete(sender, instance, **kwargs):
    instance.picture.delete(False)

# TODO : vue contact