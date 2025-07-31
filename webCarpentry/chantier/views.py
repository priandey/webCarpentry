import logging
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import requests
import time
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
    # Add timestamp for time-based bot detection
    context = {
        'timestamp': int(time.time())
    }
    return render(request, 'chantier/contact.html', context)


def send_email(request):
    if request.method == "POST":
        # Honeypot check - if the hidden field is filled, it's likely a bot
        honeypot_field = request.POST.get('website', '')
        honeypot_pronouns = request.POST.get('pronouns', '')
        fake_submit = request.POST.get('fake_submit', '')
        timestamp = request.POST.get('timestamp', '')

        # Time-based bot detection (if form was submitted too quickly)
        current_time = int(time.time())
        if timestamp:
            try:
                form_time = int(timestamp)
                # If form was submitted in less than 3 seconds, likely a bot
                if current_time - form_time < 3:
                    logging.warning("Bot detected! Form submitted too quickly: %s seconds", current_time - form_time)
                    return redirect("home")
            except ValueError:
                pass

        # If honeypot fields are filled or fake submit was clicked, block the submission
        if honeypot_field or honeypot_pronouns or fake_submit:
            # Log the bot attempt (optional - you could add logging here)
            logging.warning(
                "Bot detected! Honeypot field: '%s', Phone: '%s', Fake submit: '%s'",
                honeypot_field,
                honeypot_pronouns,
                fake_submit,
            )
            # Return a success response to the bot so it thinks the form worked
            return redirect("home")

        # Check if required fields are present
        required_fields = ['subject', 'fname', 'lname', 'message', 'email']
        for field in required_fields:
            if not request.POST.get(field):
                return HttpResponse("Missing required fields", status=400)

        subject = request.POST['subject'] + " - " + request.POST['fname'] + ' ' + request.POST['lname']
        message = request.POST['message']
        from_email = request.POST['email']
        to_email = ["Leo Milliard <leo10e9@gmail.com>"]
        bcc_email = ["Pierre Riandey <riandeypierre@gmail.com>"]
        if settings.DEBUG:
            logging.warning("Sending email to %s", from_email)
            logging.warning("Subject: %s", subject)
            logging.warning("Message: %s", message)
            logging.warning("From email: %s", from_email)
            logging.warning("To email: %s", to_email)
            logging.warning("Bcc email: %s", bcc_email)
        else:
            try:
                requests.post(
                    "https://api.eu.mailgun.net/v3/mails.priandey.eu/messages",
                    auth=("api", settings.MAILGUN_API_KEY),
                    data={
                        "from": "Leocharpente.fr Form Contact <postmaster@mails.priandey.eu>",
                        "to": to_email,
                        "bcc": bcc_email,
                        "subject": subject,
                        "text": from_email + "\n" + message
                    }
                )
            except Exception:
                return HttpResponse("Could send email, please try again later.")
        return redirect("home")
    else:
        return HttpResponse("No Post Request")
