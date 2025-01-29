from django.shortcuts import render, redirect
from base.models import Chapter, MainProfile, TrainingSession, TrainingSessionProfile
from datetime import datetime
from django.urls import reverse
from urllib.parse import urlencode

def chapter_profiles_view(request):
    # Get all chapters
    chapters = Chapter.objects.all()
    profiles = None  # No profiles initially
    selected_profiles_ids = request.session.get('selected_profiles', [])
    selected_dates = request.session.get('selected_dates', {})

    # Get all training sessions' names
    training_sessions = TrainingSession.objects.all()

    if request.method == 'POST':
        chapter_id = request.POST.get('chapter')
        if chapter_id:
            chapter = Chapter.objects.get(id=chapter_id)
            # Exclude profiles that are already added to the selected profiles
            profiles = MainProfile.objects.filter(Chapter=chapter.name).exclude(id__in=selected_profiles_ids)

        # Handle adding profiles to selected profiles list (append without replacing)
        if 'add_profiles' in request.POST:
            new_selected_profiles_ids = request.POST.getlist('selected_profiles')
            # Append the new selected profiles to the existing list, avoiding duplicates
            selected_profiles_ids = list(set(selected_profiles_ids + new_selected_profiles_ids))
            request.session['selected_profiles'] = selected_profiles_ids

            # Add default date for each added profile
            for profile_id in new_selected_profiles_ids:
                if profile_id not in selected_dates:
                    selected_dates[profile_id] = datetime.now().strftime("%Y-%m-%d")
            request.session['selected_dates'] = selected_dates

            # Redirect to the same page to show the updated data
            return redirect('chapter_profiles')

        # Handle updating the date for all selected profiles
        if 'update_dates' in request.POST:
            date_value = request.POST.get('date_all')
            training_session_id = request.POST.get('training_session')

            if date_value:
                # Print the selected date and training session to the console
                print(f"Selected Date: {date_value}")
                
                if training_session_id:
                    training_session = TrainingSession.objects.get(id=training_session_id)
                    print(f"Selected Training Session: {training_session.training_name} on {training_session.date}")
                
                # Apply the selected date to all profiles
                for profile_id in selected_profiles_ids:
                    selected_dates[profile_id] = date_value
                request.session['selected_dates'] = selected_dates

                # Print selected profiles to the console
                selected_profiles = MainProfile.objects.filter(id__in=selected_profiles_ids)
                print("Selected Profiles:")
                for profile in selected_profiles:
                    print(f" - {profile.first_name} {profile.last_name}")

                # Save the TrainingSessionProfile records, ensuring uniqueness
                for profile_id in selected_profiles_ids:
                    profile = MainProfile.objects.get(id=profile_id)
                    training_session = TrainingSession.objects.get(id=training_session_id)

                    # Check if the combination of training_session and selected_date already exists
                    if not TrainingSessionProfile.objects.filter(training_session=training_session, selected_date=date_value, user=profile).exists():
                        TrainingSessionProfile.objects.create(
                            user=profile,
                            training_session=training_session,
                            selected_date=date_value
                        )
                    else:
                        print(f"Duplicate entry found for {profile.first_name} {profile.last_name} on {date_value} for {training_session.training_name}")

        # Clear individual profile from selected profiles
        if 'clear_profile' in request.POST:
            profile_id_to_clear = request.POST.get('clear_profile')
            selected_profiles_ids = [profile_id for profile_id in selected_profiles_ids if profile_id != profile_id_to_clear]
            del selected_dates[profile_id_to_clear]
            request.session['selected_profiles'] = selected_profiles_ids
            request.session['selected_dates'] = selected_dates

        # Clear all selected profiles
        if 'clear_all' in request.POST:
            selected_profiles_ids = []
            selected_dates = {}
            request.session['selected_profiles'] = selected_profiles_ids
            request.session['selected_dates'] = selected_dates

    # Get the selected profiles using the stored IDs
    selected_profiles = MainProfile.objects.filter(id__in=selected_profiles_ids) if selected_profiles_ids else []

    return render(request, 'training_sessions/chapter_profiles.html', {
        'chapters': chapters,
        'profiles': profiles,
        'selected_profiles': selected_profiles,
        'selected_profiles_ids': selected_profiles_ids,
        'selected_dates': selected_dates,
        'training_sessions': training_sessions,
    })


from django.shortcuts import render, redirect, get_object_or_404
from base.models import Chapter, MainProfile, TrainingSession, TrainingSessionProfile
from datetime import datetime

def edit_training_session_view(request):
    # Fetch available training sessions and chapters
    training_sessions = TrainingSession.objects.all()
    chapters = Chapter.objects.all()

    # Get selected values
    selected_training_id = request.GET.get('training_session')
    selected_date = request.GET.get('date')
    selected_chapter_id = request.GET.get('chapter')

    profiles = []
    all_profiles = []

    # Ensure we have selected a training session and date
    if selected_training_id and selected_date:
        training_session = get_object_or_404(TrainingSession, id=selected_training_id)
        profiles = TrainingSessionProfile.objects.filter(training_session=training_session, selected_date=selected_date)

        # Filter available profiles based on chapter
        if selected_chapter_id:
            selected_chapter = get_object_or_404(Chapter, id=selected_chapter_id)
            all_profiles = MainProfile.objects.filter(Chapter=selected_chapter.name).exclude(
                id__in=profiles.values_list('user__id', flat=True)
            )
        elif selected_chapter_id != None:
            print(selected_chapter_id)
            all_profiles = MainProfile.objects.exclude(id__in=profiles.values_list('user__id', flat=True))

    if request.method == 'POST':
        if 'add_profiles' in request.POST:
            new_selected_profiles_ids = request.POST.getlist('selected_profiles')

            for profile_id in new_selected_profiles_ids:
                profile = get_object_or_404(MainProfile, id=profile_id)

                # Prevent duplicate entries
                if not TrainingSessionProfile.objects.filter(training_session=training_session, selected_date=selected_date, user=profile).exists():
                    TrainingSessionProfile.objects.create(
                        user=profile,
                        training_session=training_session,
                        selected_date=selected_date
                    )

        if 'delete_profile' in request.POST:
            profile_id_to_remove = request.POST.get('delete_profile')
            TrainingSessionProfile.objects.filter(id=profile_id_to_remove).delete()

        if 'clear_all' in request.POST:
            profiles.delete()

        # After adding or deleting profiles, retain selected values
        base_url = reverse('edit_training_session')
        query_params = {
            'training_session': selected_training_id,
            'date': selected_date,
            'chapter': selected_chapter_id
        }
        return redirect(f"{base_url}?{urlencode(query_params)}")

    return render(request, 'training_sessions/edit_training_session.html', {
        'training_sessions': training_sessions,
        'chapters': chapters,
        'selected_training_id': selected_training_id,
        'selected_date': selected_date,
        'selected_chapter_id': selected_chapter_id,
        'profiles': profiles,
        'all_profiles': all_profiles
    })
