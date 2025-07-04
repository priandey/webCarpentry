from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import requests
from .models import Chantier, Picture


def index(request):
    chantiers = Chantier.objects.all().order_by('-date_of_work')
    return render(request, 'chantier/index.html', {"chantiers": chantiers})


def chantier(request, pk):
    chantier = get_object_or_404(Chantier, pk=pk)
    all_pictures = Picture.objects.filter(chantier=chantier).order_by('pk')
    return render(request, 'chantier/single.html', {"chantier": chantier, "all_pictures": all_pictures})


def bio(request):
    return render(request, 'chantier/bio.html')


def contact(request):
    return render(request, 'chantier/contact.html')


def send_email(request):
    if request.method == "POST":
        subject = request.POST['subject'] + " - " + request.POST['fname'] + ' ' + request.POST['lname']
        message = request.POST['message']
        from_email = request.POST['email']
        try:
            requests.post(
                "https://api.eu.mailgun.net/v3/mails.priandey.eu/messages",
                auth=("api", settings.MAILGUN_API_KEY),
                data={
                    "from": "Leocharpente.fr Form Contact <postmaster@mails.priandey.eu>",
                    "to": ["Leo Milliard <leo10e9@gmail.com>"],
                    "bcc": ["Pierre Riandey <riandeypierre@gmail.com>"],
                    "subject": subject,
                    "text": from_email + "\n" + message
                }
            )
        except Exception:
            return HttpResponse("Could send email, please try again later.")
        return redirect("home")
    else:
        return HttpResponse("No Post Request")
