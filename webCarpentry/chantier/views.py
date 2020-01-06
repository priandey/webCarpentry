from django.shortcuts import render, get_object_or_404
from .models import Chantier


def index(request):
    chantiers = Chantier.objects.all().order_by('-date_of_work')
    return render(request, 'chantier/index.html', locals())


def chantier(request, pk):
    chantier = get_object_or_404(Chantier, pk=pk)
    return render(request, 'chantier/single.html', locals())

def bio(request):
    return render(request, 'chantier/bio.html', locals())

