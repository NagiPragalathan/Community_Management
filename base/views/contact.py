from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from base.models import ContactFormSubmission  # Assuming you have a model to store form submissions

def contact_form(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        message = request.POST.get('message')

        # Save the form data to the database
        contact_submission = ContactFormSubmission.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            country=country,
            message=message
        )

        # Send an email to the admin
        send_mail(
            subject=f"New Contact Form Submission from {first_name} {last_name}",
            message=f"Name: {first_name} {last_name}\nEmail: {email}\nPhone: {phone_number}\nCountry: {country}\nMessage: {message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        return render(request, 'success.html')

    return render(request, 'contact.html')

def subscription_expired(request):
    return render(request, 'subscription_expired.html')