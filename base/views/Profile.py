from django.shortcuts import render, redirect, get_object_or_404
from base.models import MainProfile, ContactDetails, UserProfile, Address, BillingAddress, Bio, Gallery, ChapterName, Chapter
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password


def is_admin_user(user):
    """
    Check if the user is a superuser or has staff permissions
    """
    return user.is_superuser or user.is_staff


def profile_management(request):
    return render(request, 'Profile/profile_management.html')

def add_profile(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        title = request.POST.get('title', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        suffix = request.POST.get('suffix', '')

        display_name = request.POST.get('display_name', '')
        gender = request.POST.get('gender', '')
        company_name = request.POST.get('company_name', '')
        product_service_description = request.POST.get('product_service_description', '')
        gst_registered_state = request.POST.get('gst_registered_state', '')
        gst_identification_number_or_pan = request.POST.get('gst_identification_number_or_pan', '')
        industry = request.POST.get('industry', '')
        classification = request.POST.get('classification', '')
        requested_speciality = request.POST.get('requested_speciality', '')
        membership_status = request.POST.get('membership_status', 'Active')
        my_business = request.POST.get('my_business', '')
        keywords = request.POST.get('keywords', '')

        # Handling renewal_due_date conversion (fixing the format issue)
        renewal_due_date = request.POST.get('renewal_due_date', None)
        
        chapter_name_value = request.POST.get('chapter_display', None)
        chapter_instance = None
        if chapter_name_value:
            chapter_instance = get_object_or_404(ChapterName, id=chapter_name_value)

        # Update user details
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update or create MainProfile
        profile, created = MainProfile.objects.update_or_create(
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
                'renewal_due_date': renewal_due_date,
                'Chapter': chapter_instance,
                'my_business': my_business,
                'keywords': keywords
            }
        )

        messages.success(request, 'Profile added successfully.')
        return redirect('add_profile', username=username)

    # Ensure `base_template` is always set correctly
    is_admin = is_admin_user(request.user)
    base_template = 'dummy_base_dont_remove_this_file.html' if is_admin else 'base.html'

    try:
        if not is_admin:
            profile = MainProfile.objects.get(user=request.user)
            chapter = None if not is_admin else ChapterName.objects.all()
        else:
            profile =  MainProfile.objects.get(user=User.objects.get(username=username))
            chapter = ChapterName.objects.all()
        return render(request, 'Profile/add_profile.html', {
            'data': profile,
            'chapter': chapter,
            'is_admin': is_admin,
            'base_template': base_template,
        })
    except MainProfile.DoesNotExist:
        # Show error message if profile does not exist
        messages.error(request, "Contact your admin to ask to initialize the main profile. Thanks.")
        profile = MainProfile.objects.filter(user=request.user).first()
        chapters = Chapter.objects.filter(name=profile.Chapter.id).first()

        return render(request, 'Profile/add_profile.html', {
            'data': None,
            'chapter': chapters,
            'is_admin': is_admin,
            'error': True,
            'base_template': base_template,
            'is_admin': is_admin_user(request.user)
        })


def add_contact_details(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        show_on_bni_public_websites = request.POST.get('show_on_bni_public_websites') == 'on'

        receive_updates_from_bni = request.POST.get('receive_updates_from_bni') == 'on'
        share_revenue_data_with_bni_director = request.POST.get('share_revenue_data_with_bni_director') == 'on'
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
        website = request.POST.get('website', '')
        social_networking_links = request.POST.get('social_networking_links', '')

        contact_details, created = ContactDetails.objects.update_or_create(
            user=user,
            defaults={
                'show_on_bni_public_websites': show_on_bni_public_websites,
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
                'social_networking_links': social_networking_links
            }
        )

        messages.success(request, 'Contact details added successfully.')
        return redirect('add_contact_details', username=username)

    try:
        contact_details = ContactDetails.objects.get(user=User.objects.get(username=username))
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

    # Ensure base_template is always set
    base_template = 'dummy_base_dont_remove_this_file.html' if is_admin_user(request.user) else 'base.html'
    
    return render(request, 'Profile/add_contact_details.html', {"initial_data": initial_data, "base_template": base_template})


def add_edit_user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        language = request.POST.get('language', '')
        timezone = request.POST.get('timezone', '')
        profile_image = request.FILES.get('profile_image')
        company_logo = request.FILES.get('company_logo')
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if user_profile and not is_admin_user(request.user):  # Editing existing profile
            user_profile.language = language
            user_profile.timezone = timezone
            if profile_image:
                user_profile.profile_image = profile_image
            if company_logo:
                user_profile.company_logo = company_logo
            user_profile.save()
            messages.success(request, "Profile updated successfully.")
        else:  # Creating a new user and profile
            if User.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists.")
                return redirect('add_edit_user_profile')

            user = User.objects.create(
                username=username,
                email=email,
            )
            user.set_password(password)  # Hash the password
            user.save()

            user_profile = UserProfile.objects.create(
                user=user,
                language=language,
                timezone=timezone,
                profile_image=profile_image,
                company_logo=company_logo
            )
            user_profile.save()
            messages.success(request, "New user profile created successfully.")

        return redirect('add_edit_user_profile')

    base_template = 'dummy_base_dont_remove_this_file.html' if is_admin_user(request.user) else 'base.html'

    return render(request, 'Profile/add_edit_user_profile.html', {
        'user_profile': None if is_admin_user(request.user) else user_profile,
        'base_template': base_template,
        'is_admin': not is_admin_user(request.user)
    })


@login_required
def add_or_edit_address(request, username):
    user = User.objects.get(username=username)
    is_admin = is_admin_user(request.user)
    print("user :", user)
    try:
        address = Address.objects.filter(user=user, address_type="Address").first()  # Use `.first()` instead of try-except
        billing = BillingAddress.objects.filter(user=user).first()
    except Exception as e:
        print(e)
        address = None
        billing = None
    
    print(address)
    print(billing)


    if request.method == 'POST':

        address_type = request.POST.get('address_type', None)
        address_data = {
            'address_line_1': request.POST.get('address_line_1', '').strip(),
            'address_line_2': request.POST.get('address_line_2', '').strip(),
            'city': request.POST.get('city', '').strip(),
            'state': request.POST.get('state', '').strip(),
            'country': request.POST.get('country', '').strip(),
            'zip_code': request.POST.get('zip_code', '').strip(),
        }

        try:
            if address_type:  # Handling regular address
                address, created = Address.objects.update_or_create(
                    user=user,
                    address_type=address_type,
                    defaults=address_data
                )
            else:  # Handling billing address
                billing, created = BillingAddress.objects.update_or_create(
                    user=user,
                    defaults=address_data
                )

            if created:
                messages.success(request, 'Address created successfully.')
            else:
                messages.success(request, 'Address updated successfully.')

        except Exception as e:
            messages.error(request, f'Error updating address: {str(e)}')

        return redirect('add_or_edit_address', username=username)
    else:

        # Ensure base_template is always set
        base_template = 'dummy_base_dont_remove_this_file.html' if is_admin else 'base.html'

        # Context dictionary
        context = {
            'address': address,
            'billing': billing,
            'is_admin': is_admin,
            'base_template': base_template,
            'user': user,
        }
        return render(request, 'Profile/add_or_edit_address.html', context)


def add_or_edit_bio(request, username):
    user = User.objects.get(username=username)
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
        hobbies_and_interests = request.POST.get('hobbies_interests', '')
        city_of_residence = request.POST.get('city_residence', '')
        years_in_city = int(request.POST.get('years_in_city', ''))
        burning_desire = request.POST.get('burning_desire', '')
        something_no_one_knows = request.POST.get('something_unknown', '')

        key_to_success = request.POST.get('key_to_success', '')
        
        print(hobbies_and_interests)

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

        return redirect('add_or_edit_bio', username=username)

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


def iframe(request, username):
    return render(request, 'iframe.html', {'username': username})

def email(request):
    return render(request, 'email.html')

def portal(request):
    return render(request, 'portal.html')

