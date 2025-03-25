from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from .models import Chantier, Picture


def index(request):
    chantiers = Chantier.objects.all().order_by('-date_of_work')
    return render(request, 'chantier/index.html', locals())


def chantier(request, pk):
    chantier = get_object_or_404(Chantier, pk=pk)
    all_pictures = Picture.objects.filter(chantier=chantier).order_by('pk')
    return render(request, 'chantier/single.html', locals())


def bio(request):
    return render(request, 'chantier/bio.html', locals())


def contact(request):
    return render(request, 'chantier/contact.html')


def send_email(request):
    if request.method == "POST":
        subject = request.POST['subject'] + " - " + request.POST['fname'] + ' ' + request.POST['lname']
        message = request.POST['message']
        from_email = request.POST['email']
        try:
            send_mail(subject, message, from_email, ["riandeypierre@gmail.com"])
        except BadHeaderError:
            return HttpResponse("Invalid Header Found.")
        return redirect("home")
    else:
        return HttpResponse("No Post Request")
