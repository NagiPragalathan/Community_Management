from django.shortcuts import render, redirect, get_object_or_404
from base.models import MainProfile, ContactDetails, UserProfile, Address, BillingAddress, Bio, Gallery, ChapterName
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def profile_management(request):
    return render(request, 'profile/profile_management.html')

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
        chapter = ChapterName.objects.all()
        return render(request, 'profile/add_profile.html', {'data':profile, 'chapter':chapter})
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
                'social_networking_links':social_networking_links
            }
        )
        
        messages.success(request, 'Contact details added successfully.')
        return redirect('add_contact_details')
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
            'social_networking_links': contact_details.social_networking_links
        }
        
    except ContactDetails.DoesNotExist:
        initial_data = {}

    return render(request, 'profile/add_contact_details.html', {"initial_data":initial_data})


def add_edit_user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user = request.user
        language = request.POST['language']
        timezone = request.POST['timezone']
        profile_image = request.FILES.get('profile_image')
        company_logo = request.FILES.get('company_logo')
        print(profile_image, company_logo)
        
        if user_profile:  # If editing existing profile
            user_profile.language = language
            user_profile.timezone = timezone
            if profile_image:
                user_profile.profile_image = profile_image
            if company_logo:
                user_profile.company_logo = company_logo
            user_profile.save()
        else:  # If adding new profile
            user_profile = UserProfile(user=user, language=language, timezone=timezone,
                                       profile_image=profile_image, company_logo=company_logo)
            user_profile.save()
        
        return redirect('add_edit_user_profile')
    else:
        return render(request, 'Profile/add_edit_user_profile.html', {'user_profile': user_profile})
    
    
@login_required
def add_or_edit_address(request):
    user = request.user
    try:
        address, created = Address.objects.get_or_create(
            user=user,
            address_type="Address",
            defaults={
                'address_line_1': 'Default Address Line 1',
                'address_line_2': 'Default Address Line 2',
                'city': 'Default City',
                'state': 'Default State',
                'country': 'Default Country',
                'zip_code': 'Default Zip Code'
            }
        )
    except:
        address = None
    try:
        billing, created = BillingAddress.objects.get_or_create(
            user=user,
            defaults={
                'address_line_1': 'Default Address Line 1',
                'address_line_2': 'Default Address Line 2',
                'city': 'Default City',
                'state': 'Default State',
                'country': 'Default Country',
                'zip_code': 'Default Zip Code'
            }
        )
    except Exception as e:
        billing = None
        print(e)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
    if request.method == 'POST':
        address_type = request.POST.get('address_type')
        print(address_type)
        if address_type:
            address = Address.objects.get(user=user, address_type=address_type)
        else:
            address = BillingAddress.objects.get(user=user)
        
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        
        if address:
            # If address already exists, update its fields
            try:
                address.address_type = address_type
            except:
                pass
            address.address_line_1 = address_line_1
            address.address_line_2 = address_line_2
            address.city = city
            address.state = state
            address.country = country
            address.zip_code = zip_code
            address.save()
        else:
            # If address does not exist, create a new one
            Address.objects.create(
                user=user,
                address_type=address_type,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                country=country,
                zip_code=zip_code
            )
        
        messages.success(request, 'Address added successfully.')
        return redirect('add_or_edit_address')
    
    return render(request, 'Profile/add_or_edit_address.html', {'address': address, "billing":billing})


def add_or_edit_bio(request):
    user = request.user
    try:
        bio = Bio.objects.get(user=user)
    except Bio.DoesNotExist:
        bio = None

    if request.method == 'POST':
        years_in_business = request.POST.get('years_in_business', '')
        previous_jobs = request.POST.get('previous_jobs', '')
        spouse = request.POST.get('spouse', '')
        children = request.POST.get('children', '')
        pets = request.POST.get('pets', '')
        hobbies_and_interests = request.POST.get('hobbies_and_interests', '')
        city_of_residence = request.POST.get('city_of_residence', '')
        years_in_city = int(request.POST.get('years_in_city', ''))
        burning_desire = request.POST.get('burning_desire', '')
        something_no_one_knows = request.POST.get('something_no_one_knows', '')
        key_to_success = request.POST.get('key_to_success', '')

        if bio:
            bio.years_in_business = years_in_business
            bio.previous_jobs = previous_jobs
            bio.spouse = spouse
            bio.children = children
            bio.pets = pets
            bio.hobbies_and_interests = hobbies_and_interests
            bio.city_of_residence = city_of_residence
            bio.years_in_city = years_in_city
            bio.burning_desire = burning_desire
            bio.something_no_one_knows = something_no_one_knows
            bio.key_to_success = key_to_success
            bio.save()
        else:
            bio = Bio.objects.create(
                user=user,
                years_in_business=years_in_business,
                previous_jobs=previous_jobs,
                spouse=spouse,
                children=children,
                pets=pets,
                hobbies_and_interests=hobbies_and_interests,
                city_of_residence=city_of_residence,
                years_in_city=years_in_city,
                burning_desire=burning_desire,
                something_no_one_knows=something_no_one_knows,
                key_to_success=key_to_success
            )
        
        return redirect('add_or_edit_bio')

    return render(request, 'Profile/add_or_edit_bio.html', {'bio': bio})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Gallery >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def add_gallery(request):
    user = request.user
    if request.method == 'POST':
        images = request.FILES.getlist('images')  # Changed to getlist to handle multiple files
        for image in images:
            Gallery.objects.create(user=user, image=image)  # Create a new Gallery object for each image
        return redirect('add_gallery')
    galleries = Gallery.objects.filter(user=user)  # Fetch all images for the user
    return render(request, 'Profile/add_gallery.html', {'galleries': galleries})


def delete_image(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        try:
            image = Gallery.objects.get(id=image_id)
            image.delete()
            return JsonResponse({'success': 'Image deleted successfully'})
        except Gallery.DoesNotExist:
            return JsonResponse({'error': 'Image not found'})
    return JsonResponse({'error': 'Invalid request'})
