from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from base.models import TrainingSessionProfile, TrainingSession, MainProfile, ContactDetails

def is_admin_user(user):
    """
    Check if the user is a superuser or has staff permissions
    """
    return user.is_superuser or user.is_staff

def training_sessions_report(request):
    training_sessions = TrainingSession.objects.all()
    selected_from_date = None
    selected_to_date = None
    selected_training_types = []

    members_data = []

    if request.method == 'POST':
        selected_from_date = request.POST.get('from_date')
        selected_to_date = request.POST.get('to_date')
        selected_training_types = request.POST.getlist('training_types')

        # Convert string dates to datetime objects
        if selected_from_date:
            from_date = datetime.strptime(selected_from_date, "%Y-%m-%d").date()
        else:
            from_date = None
        
        if selected_to_date:
            to_date = datetime.strptime(selected_to_date, "%Y-%m-%d").date()
        else:
            to_date = None

        # Filter TrainingSessionProfiles based on selected criteria
        query = Q()

        if selected_training_types:
            query &= Q(training_session__training_name__in=selected_training_types)
        
        if from_date and to_date:
            query &= Q(selected_date__range=[from_date, to_date])
        elif from_date:
            query &= Q(selected_date__gte=from_date)
        elif to_date:
            query &= Q(selected_date__lte=to_date)

        # Fetch data based on the query
        filtered_sessions = TrainingSessionProfile.objects.filter(query).select_related('user', 'training_session')

        for session in filtered_sessions:
            # Get the related User instance through the MainProfile instance
            user_instance = session.user.user  # Access the User model through MainProfile

            # Fetch the associated contact details using the User instance
            contact_details = ContactDetails.objects.filter(user=user_instance).first()

            members_data.append({
                'member_name': f'{session.user.first_name} {session.user.last_name}',
                'event_date': session.selected_date.strftime("%d-%b-%Y"),
                'event_type': session.training_session.training_name,
                'role': session.user.membership_status,  # You can modify this if role needs to be something specific
                'join_date': user_instance.date_joined.strftime("%d-%b-%Y") if user_instance.date_joined else "N/A",  # Access join_date from User model
                'phone': contact_details.phone if contact_details else "N/A",
                'email': contact_details.email if contact_details else "N/A"
            })

    return render(request, 'reports/training_sessions_report/training_sessions_report.html', {
        'training_sessions': training_sessions,
        'members_data': members_data,
        'selected_from_date': selected_from_date,
        'selected_to_date': selected_to_date,
        'selected_training_types': selected_training_types,
        'is_admin': is_admin_user(request.user),
        'base_template': 'admin_base.html' if is_admin_user(request.user) else 'base.html',
    })
