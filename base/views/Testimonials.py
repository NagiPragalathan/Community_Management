from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import Testimonial
from django.contrib.auth.models import User

@login_required
def give_testimonial(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)
    
    if request.method == 'POST':
        # Extract testimonial content from the form
        testimonial_content = request.POST.get('testimonial_content')
        print("testimonial_content",testimonial_content)
        # Check if a testimonial from the current user to the receiver already exists
        existing_testimonial = Testimonial.objects.filter(from_user=request.user, to_user=receiver, type='give_testimonials').exists()
        if existing_testimonial:
            # If a testimonial already exists, display an error message or handle it as desired
            print("You have already given a testimonial to this user.")
            messages.error(request, 'You have already given a testimonial to this user.')
            return redirect('connections')  # Redirect to the appropriate URL

        # Create the testimonial
        testimonial = Testimonial.objects.create(
            testimonials=testimonial_content,
            from_user=request.user,
            to_user=receiver,
            type='give_testimonials'
        )
        print("testimonial given to", receiver.username)
        
        # Optionally, you can send a notification to the receiver that they have received a new testimonial
        
        # Redirect the user to a success page or back to the profile page
        messages.success(request, 'Testimonial successfully given.')
        return redirect('connections')

    else:
        # Render a form for giving testimonials
        return render(request, 'testimonial/give_testimonial.html', {"receiver_id": receiver_id})
    
    
def incoming_testimonials(request, username=None):
    if username:
        current_user = User.objects.get(username=username)
    else:
        current_user = request.user


    for i in Testimonial.objects.all():
        print(i.from_user.username, i.to_user.username)

    # Filter testimonials where the to_user is the current user
    incoming_testimonials = Testimonial.objects.filter(to_user=current_user).exclude(type='req_testimonials')

    # Pass the incoming testimonials to the template for rendering
    return render(request, 'testimonial/incoming_testimonials.html', {'incoming_testimonials': incoming_testimonials})

@login_required
def request_testimonial(request, receiver_id):
    # Get the recipient user object or return a 404 error if not found
    receiver_user = get_object_or_404(User, id=receiver_id)
    
    # Check if a testimonial request already exists from the current user to the specified user
    existing_request = Testimonial.objects.filter(from_user=request.user, to_user=receiver_user, type='req_testimonials').exists()
    
    if existing_request:
        # If a request already exists, display an error message or handle it as desired
        print("You have already requested a testimonial from this user.")
        messages.error(request, 'You have already requested a testimonial from this user.')
        return redirect('connections')  # Redirect to the appropriate URL
    
    if request.method == 'POST':
        from_user = request.user
        to_user_id = receiver_id  # Assuming you pass the user_id of the recipient in the URL
        message = request.POST.get('message')  # Assuming you have a form field for entering a message

        # Create a new testimonial request
        testimonial_request = Testimonial.objects.create(
            from_user=from_user,
            to_user=receiver_user,
            type='req_testimonials',
            testimonials=message
        )

        # Optionally, you can add a success message
        messages.success(request, 'Testimonial request sent successfully.')
        for i in Testimonial.objects.all():
            print(i.from_user)

        return redirect('request_testimonial', receiver_id)  # Redirect to the user's profile page or any other desired URL

    # If the request method is not POST, render the template with a form to request testimonials
    return render(request, 'testimonial/request_testimonial.html')


def list_requested_testimonials(request):
    # Filter testimonials where type is 'req_testimonials'
    requested_testimonials = Testimonial.objects.filter(type='req_testimonials', from_user=request.user)

    # Pass the queryset to the template for rendering
    return render(request, 'testimonial/list_requested_testimonials.html', {'requested_testimonials': requested_testimonials})

def list_inboxrequested_testimonials(request):
    # Filter testimonials where type is 'req_testimonials'
    requested_testimonials = Testimonial.objects.filter(type='req_testimonials', to_user=request.user)
    
    for i in Testimonial.objects.all():
        print(i.type, i.to_user, i.from_user)
    print(requested_testimonials)

    # Pass the queryset to the template for rendering
    return render(request, 'testimonial/list_requested_testimonials.html', {'requested_testimonials': requested_testimonials})

def menuOfTestimonial(request):
    return render(request, 'testimonial/menuoftest.html')

