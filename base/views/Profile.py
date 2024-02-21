from django.shortcuts import render, redirect
from base.models import MainProfile, ContactDetails, SocialNetworkingLink
from django.contrib.auth.models import User
from django.contrib import messages

def add_profile(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title', 'title')
        first_name = request.POST.get('first_name', 'first_name')
        last_name = request.POST.get('last_name', 'last_name')
        suffix = request.POST.get('suffix', 'suffix')
        display_name = request.POST.get('display_name', 'display_name')
        gender = request.POST.get('gender', 'gender')
        company_name = request.POST.get('company_name', 'company_name')
        product_service_description = request.POST.get('product_service_description', 'product_service_description')
        gst_registered_state = request.POST.get('gst_registered_state'), 'gst_registered_state'
        gst_identification_number_or_pan = request.POST.get('gst_identification_number_or_pan', 'gst_identification_number_or_pan')
        industry = request.POST.get('industry', 'industry')
        classification = request.POST.get('classification', 'classification')
        requested_speciality = request.POST.get('requested_speciality', 'requested_speciality')
        membership_status = request.POST.get('membership_status', 'membership_status')
        renewal_due_date = request.POST.get('renewal_due_date', 'renewal_due_date')
        chapter = request.POST.get('chapter'), 'chapter'
        my_business = request.POST.get('my_business', 'my_business')
        keywords = request.POST.get('keywords', 'keywords')

        MainProfile.objects.update_or_create(
            user=user,
            defaults={
                'title': title,
                'first_name': first_name,
                'last_name': last_name,
                'suffix': suffix,
                'display_name': display_name,
                'gender': gender,
                'company_name': company_name,
                'product_service_description': product_service_description,
                'gst_registered_state': gst_registered_state,
                'gst_identification_number_or_pan': gst_identification_number_or_pan,
                'industry': industry,
                'classification': classification,
                'requested_speciality': requested_speciality,
                'membership_status': membership_status,
                'RenewalDueDate': renewal_due_date,
                'Chapter': chapter,
                'my_business': my_business,
                'keywords': keywords
            }
        )


        messages.success(request, 'Profile added successfully.')
    try:
        profile = MainProfile.objects.get(user=request.user)
        return render(request, 'profile/add_profile.html', {'data':profile})
    except:
        return render(request, 'profile/add_profile.html')
        

def add_contact_details(request):
    if request.method == 'POST':
        user = request.user
        show_on_bni_public_websites = request.POST.get('show_on_bni_public_websites', False)
        billing_address_quick_copy = request.POST.get('billing_address_quick_copy', '')
        phone = request.POST.get('phone', '')
        direct_number = request.POST.get('direct_number', '')
        home = request.POST.get('home', '')
        mobile_number = request.POST.get('mobile_number', '')
        pager = request.POST.get('pager', '')
        voice_mail = request.POST.get('voice_mail', '')
        toll_free = request.POST.get('toll_free', '')
        fax = request.POST.get('fax', '')
        email = request.POST.get('email', '')
        receive_updates_from_bni = request.POST.get('receive_updates_from_bni', False)
        share_revenue_data_with_bni_director = request.POST.get('share_revenue_data_with_bni_director', False)
        website = request.POST.get('website', '')
        social_networking_links = request.POST.getlist('social_networking_links')
        social_networking_link_ids = request.POST.getlist('social_networking_links')
        social_networking_links = SocialNetworkingLink.objects.filter(id__in=social_networking_link_ids)

        contact_details, created = ContactDetails.objects.update_or_create(
            user=user,
            defaults={
                'show_on_bni_public_websites': True if show_on_bni_public_websites else False,
                'billing_address_quick_copy': billing_address_quick_copy,
                'phone': phone,
                'direct_number': direct_number,
                'home': home,
                'mobile_number': mobile_number,
                'pager': pager,
                'voice_mail': voice_mail,
                'toll_free': toll_free,
                'fax': fax,
                'email': email,
                'receive_updates_from_bni': receive_updates_from_bni,
                'share_revenue_data_with_bni_director': share_revenue_data_with_bni_director,
                'website': website,
            }
        )
        contact_details.social_networking_links.add(*social_networking_links)
        
        messages.success(request, 'Contact details added successfully.')
        return redirect('profile:view_contact_details')
    try:
        contact_details = ContactDetails.objects.get(user=request.user)
        initial_data = {
            'show_on_bni_public_websites': contact_details.show_on_bni_public_websites,
            'billing_address_quick_copy': contact_details.billing_address_quick_copy,
            'phone': contact_details.phone,
            'direct_number': contact_details.direct_number,
            'home': contact_details.home,
            'mobile_number': contact_details.mobile_number,
            'pager': contact_details.pager,
            'voice_mail': contact_details.voice_mail,
            'toll_free': contact_details.toll_free,
            'fax': contact_details.fax,
            'email': contact_details.email,
            'receive_updates_from_bni': contact_details.receive_updates_from_bni,
            'share_revenue_data_with_bni_director': contact_details.share_revenue_data_with_bni_director,
            'website': contact_details.website,
            'social_networking_links': [link.pk for link in contact_details.social_networking_links.all()]
        }
    except ContactDetails.DoesNotExist:
        initial_data = {}

    return render(request, 'profile/add_contact_details.html', {"initial_data":initial_data})
