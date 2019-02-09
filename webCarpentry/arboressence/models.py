from django.db import models


class Photo(models.Model):
    original_photo      = models.BinaryField()
    thumbnail_photo     = models.BinaryField()
    InSerieNumber       = models.IntegerField()

class Category(models.Model):
    name                = models.CharField(max_length=40)
    logo                = models.BinaryField()

    def __str__(self):
        return self.name

'''class ChantierAsCategory(models.Model):
    chantier            = models.ForeignKey(Chantier, on_delete=models.CASCADE)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority            = models.IntegerField(default=1)'''

class Essences(models.Model):
    name                = models.CharField(max_length=70)

    def __str__(self):
        return self.name

class Chantier(models.Model):
    name                = models.CharField(max_length=90)
    short_description   = models.CharField(max_length=250)
    localisation        = models.CharField(max_length=100)
    date_of_chantier    = models.DateTimeField()
    created_at          = models.DateTimeField(auto_now_add=True)
    category            = models.ManyToManyField(Category)
    essence             = models.ManyToManyField(Essences)
    photo               = models.ManyToManyField(Photo)

    def __str__(self):
        return self.name
'''class ChantierAsEssence(models.Model):
    chantier            = models.ForeignKey(Chantier, on_delete=models.CASCADE)
    essence             = models.ForeignKey(Essences, on_delete=models.CASCADE)'''
