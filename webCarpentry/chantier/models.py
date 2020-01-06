from django.db import models

class Chantier(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
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


# TODO : Check image rotation with Pillow when portrait eg: Echelle de Meunier
# TODO : Media not deleted after model deletion
# TODO : Signer
# TODO : vue contact