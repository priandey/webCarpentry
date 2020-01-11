from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Chantier(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_of_work = models.DateField()
    upload_date = models.DateTimeField(auto_now_add=True)
    main_picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

    @property
    def pictures_count(self):
        return(len(self.pictures.all()))


class Picture(models.Model):
    chantier = models.ForeignKey(Chantier, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255, null=True, blank=True)

@receiver(post_delete, sender=Picture)
def submission_delete(sender, instance, **kwargs):
    instance.picture.delete(False)

# TODO : vue contact