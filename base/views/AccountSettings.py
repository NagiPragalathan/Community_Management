from django.shortcuts import get_object_or_404, redirect, render
from base.models import AccountSettings
from django.http import HttpResponse
from django.contrib.auth.models import User

def is_admin_user(user):
    return user.is_superuser


def edit_or_add_account_settings(request, username=None, dashboard=0):
    context = {}
    if username != None:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = request.user
    else:
        user = request.user


    is_admin = is_admin_user(request.user)
    if request.method == 'POST':
        
        # Retrieve all values from the form
        bio_visibility = request.POST.get('bio_visibility', 'all')
        connections_visibility = request.POST.get('connections_visibility', 'all')
        testimonials_visibility = request.POST.get('testimonials_visibility', 'all')
        gallery_visibility = request.POST.get('gallery_visibility', 'all')
        email_visibility = request.POST.get('email_visibility', 'all')
        contact_details_visibility = request.POST.get('contact_details_visibility', 'all')
        post_notifications = request.POST.get('post_notifications', 'every_time')
        alternate_email = request.POST.get('alternate_email', '')
        forward_messages = request.POST.get('forward_messages', False) == 'on'
        forward_sent_mail = request.POST.get('forward_sent_mail', False) == 'on'
        forward_connection_requests = request.POST.get('forward_connection_requests', False) == 'on'
        forward_recommendation_requests = request.POST.get('forward_recommendation_requests', False) == 'on'
        country_settings_for_group_notifications = request.POST.get('country_settings_for_group_notifications', 'Default')

        account_settings, created = AccountSettings.objects.get_or_create(user=user)

        # Update or set values
        account_settings.bio_visibility = bio_visibility
        account_settings.connections_visibility = connections_visibility
        account_settings.testimonials_visibility = testimonials_visibility
        account_settings.gallery_visibility = gallery_visibility
        account_settings.email_visibility = email_visibility
        account_settings.contact_details_visibility = contact_details_visibility
        account_settings.post_notifications = post_notifications
        account_settings.alternate_email = alternate_email
        account_settings.forward_messages = forward_messages
        account_settings.forward_sent_mail = forward_sent_mail
        account_settings.forward_connection_requests = forward_connection_requests
        account_settings.forward_recommendation_requests = forward_recommendation_requests
        account_settings.country_settings_for_group_notifications = country_settings_for_group_notifications

        account_settings.save()
        if dashboard == 0:
            return redirect('edit_or_add_account_settings', username=username, dashboard=dashboard)  # Redirect to a new URL
        else:
            return redirect('edit_or_add_account_settings')  # Redirect to a new URL
    else:
        # If not a POST request, try to retrieve existing settings to pre-fill the form

        account_settings = AccountSettings.objects.filter(user=request.user).first()
        if account_settings:
            context['account_settings'] = account_settings
            is_admin = is_admin_user(request.user)
            context['is_admin'] = is_admin
            context['base_template'] = 'dummy_base_dont_remove_this_file.html' if is_admin else 'base.html'
            if dashboard != 0:
                context['base_template'] = 'dummy_base_dont_remove_this_file.html'
        print(context)
        context['base_template'] = 'dummy_base_dont_remove_this_file.html' if is_admin else 'base.html'
        if dashboard != 0:
            context['base_template'] = 'dummy_base_dont_remove_this_file.html'

        return render(request, 'Settings/edit_or_add_account_settings.html', context)
