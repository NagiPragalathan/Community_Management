from django.shortcuts import render
from django.shortcuts import render, redirect
from base.models import CityData, Group, Connection, MainProfile, oneToOneMessage, Meeting, UserProfile, ChapterEducationUnit, TYFCB, ReferralSlip, Visitor, Bio, Address
from base.form.forms import CityDataForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


def calculate_meeting_counts(user):
    # Lifetime count of meetings invited by the user
    lifetime_count = Meeting.objects.filter(invited_by=user).count()

    # Calculate the date 12 months ago from today
    twelve_months_ago = timezone.now() - timedelta(days=365)

    # Count of meetings invited by the user in the last 12 months
    last_12_months_count = Meeting.objects.filter(invited_by=user, date__gte=twelve_months_ago).count()

    # Calculate percentage
    if lifetime_count > 0:
        percentage = (last_12_months_count / lifetime_count) * 100
    else:
        percentage = 0

    return lifetime_count, last_12_months_count, percentage

def calculate_ceu_counts(user):
    # Lifetime count of CEUs
    lifetime_count = ChapterEducationUnit.objects.filter(user=user).count()

    # Calculate the date 12 months ago from today
    twelve_months_ago = timezone.now().date() - timedelta(days=365)

    # Count of CEUs in the last 12 months
    last_12_months_count = ChapterEducationUnit.objects.filter(user=user, date__gte=twelve_months_ago).count()

    # Calculate percentage
    if lifetime_count > 0:
        percentage = (last_12_months_count / lifetime_count) * 100
    else:
        percentage = 0

    return lifetime_count, last_12_months_count, percentage

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "index.html")

@login_required(login_url='/login/')
def dashboard(request):
    user = request.user
    group_count = Group.objects.filter(creator=user).count()
    connection_count = Connection.objects.filter(
        Q(user=request.user) | Q(connection=request.user), 
        status='accepted'
    ).count()
    onelifetime_count, onelast_12_months_count, onepercentage = calculate_meeting_counts(request.user)
    eculifetime_count, eculast_12_months_count, ecupercentage = calculate_ceu_counts(request.user)
    
    today = timezone.now().date()
    one_year_ago = today - timedelta(days=365)

    # Lifetime counts
    given_lifetime_count = TYFCB.objects.filter(user=user).count()
    received_lifetime_count = TYFCB.objects.filter(thank_you_to=user).count()

    # Last 12 months counts
    given_last_12_months_count = TYFCB.objects.filter(user=user, start_date__gte=one_year_ago).count()
    received_last_12_months_count = TYFCB.objects.filter(thank_you_to=user, start_date__gte=one_year_ago).count()

    # Calculate percentages
    given_percentage = (given_last_12_months_count / given_lifetime_count * 100) if given_lifetime_count > 0 else 0
    received_percentage = (received_last_12_months_count / received_lifetime_count * 100) if received_lifetime_count > 0 else 0
    
     # Lifetime counts
    Rgiven_lifetime_count = ReferralSlip.objects.filter(from_user=user).count()
    Rreceived_lifetime_count = ReferralSlip.objects.filter(to_member=user).count()

    # Last 12 months counts
    Rgiven_last_12_months_count = ReferralSlip.objects.filter(from_user=user, date__gte=one_year_ago).count()
    Rreceived_last_12_months_count = ReferralSlip.objects.filter(to_member=user, date__gte=one_year_ago).count()

    # Calculate percentages
    Rgiven_percentage = (Rgiven_last_12_months_count / Rgiven_lifetime_count * 100) if Rgiven_lifetime_count > 0 else 0
    Rreceived_percentage = (Rreceived_last_12_months_count / Rreceived_lifetime_count * 100) if Rreceived_lifetime_count > 0 else 0
    
    visitor_count = Visitor.objects.filter(user=user).count()
    visitor_last_12_months_count = Visitor.objects.filter(user=user, date__gte=one_year_ago).count()
    visitor_percentage = (visitor_last_12_months_count / visitor_count * 100) if visitor_count > 0 else 0
    
    context = {
        'group_count': group_count,
        'connection_count': connection_count,
        
        "onelifetime_count": onelifetime_count,
        "onelast_12_months_count":onelast_12_months_count,
        "onepercentage":onepercentage,
        
        "eculifetime_count":eculifetime_count,
        "eculast_12_months_count": eculast_12_months_count,
        "ecupercentage": ecupercentage,
        
        "given_lifetime_count":given_lifetime_count,
        "given_last_12_months_count":given_last_12_months_count, 
        "given_percentage": given_percentage,
        
        "received_lifetime_count":received_lifetime_count,
        "received_last_12_months_count": received_last_12_months_count,
        "received_percentage": received_percentage,
        
        'Rgiven_lifetime_count': Rgiven_lifetime_count,
        'Rgiven_last_12_months_count': Rgiven_last_12_months_count,
        'Rgiven_percentage': Rgiven_percentage,
        
        'Rreceived_lifetime_count': Rreceived_lifetime_count,
        'Rreceived_last_12_months_count': Rreceived_last_12_months_count,
        'Rreceived_percentage': Rreceived_percentage,
        
        'visitor_count': visitor_count,
        'visitor_last_12_months_count': visitor_last_12_months_count,
        'visitor_percentage': visitor_percentage,
        
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login/')
def chart_dashboard(request):
    user = request.user
    group_count = Group.objects.filter(creator=user).count()
    connection_count = Connection.objects.filter(
        Q(user=request.user) | Q(connection=request.user), 
        status='accepted'
    ).count()
    onelifetime_count, onelast_12_months_count, onepercentage = calculate_meeting_counts(request.user)
    eculifetime_count, eculast_12_months_count, ecupercentage = calculate_ceu_counts(request.user)
    
    today = timezone.now().date()
    one_year_ago = today - timedelta(days=365)

    # Lifetime counts
    given_lifetime_count = TYFCB.objects.filter(user=user).count()
    received_lifetime_count = TYFCB.objects.filter(thank_you_to=user).count()

    # Last 12 months counts
    given_last_12_months_count = TYFCB.objects.filter(user=user, start_date__gte=one_year_ago).count()
    received_last_12_months_count = TYFCB.objects.filter(thank_you_to=user, start_date__gte=one_year_ago).count()

    # Calculate percentages
    given_percentage = (given_last_12_months_count / given_lifetime_count * 100) if given_lifetime_count > 0 else 0
    received_percentage = (received_last_12_months_count / received_lifetime_count * 100) if received_lifetime_count > 0 else 0
    
     # Lifetime counts
    Rgiven_lifetime_count = ReferralSlip.objects.filter(from_user=user).count()
    Rreceived_lifetime_count = ReferralSlip.objects.filter(to_member=user).count()

    # Last 12 months counts
    Rgiven_last_12_months_count = ReferralSlip.objects.filter(from_user=user, date__gte=one_year_ago).count()
    Rreceived_last_12_months_count = ReferralSlip.objects.filter(to_member=user, date__gte=one_year_ago).count()

    # Calculate percentages
    Rgiven_percentage = (Rgiven_last_12_months_count / Rgiven_lifetime_count * 100) if Rgiven_lifetime_count > 0 else 0
    Rreceived_percentage = (Rreceived_last_12_months_count / Rreceived_lifetime_count * 100) if Rreceived_lifetime_count > 0 else 0
    
    context = {
        'group_count': group_count,
        'connection_count': connection_count,
        
        "onelifetime_count": onelifetime_count,
        "onelast_12_months_count":onelast_12_months_count,
        "onepercentage":onepercentage,
        
        "eculifetime_count":eculifetime_count,
        "eculast_12_months_count": eculast_12_months_count,
        "ecupercentage": ecupercentage,
        
        "given_lifetime_count":given_lifetime_count,
        "given_last_12_months_count":given_last_12_months_count, 
        "given_percentage": given_percentage,
        
        "received_lifetime_count":received_lifetime_count,
        "received_last_12_months_count": received_last_12_months_count,
        "received_percentage": received_percentage,
        
        'Rgiven_lifetime_count': Rgiven_lifetime_count,
        'Rgiven_last_12_months_count': Rgiven_last_12_months_count,
        'Rgiven_percentage': Rgiven_percentage,
        
        'Rreceived_lifetime_count': Rreceived_lifetime_count,
        'Rreceived_last_12_months_count': Rreceived_last_12_months_count,
        'Rreceived_percentage': Rreceived_percentage,
        
    }
    return render(request, 'chart_dashboard.html', context)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Country >>>>>>>>>>>>>>>>>>>>>>>>


# View to add a new city
def add_city(request):
    city = CityData.objects.all()
    if request.method == 'POST':
        form = CityDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_city')
    else:
        form = CityDataForm()
    return render(request, 'region/city_form.html', {'form': form, 'city':city})


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Common Data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def common_data(request):
    context = {}
    if request.user.is_authenticated:
        current_user = request.user
        usr_name = current_user.username
        try:
            profile = MainProfile.objects.get(user=current_user)
            usr_img = UserProfile.objects.get(user=current_user).profile_image
        except:
            usr_img = "none"
            profile = {}
            
        unseen_messages = oneToOneMessage.objects.filter(receiver=current_user, seen=False)
        unseen_messages_count = unseen_messages.count()

        # Annotate each message with the sender's display name
        unseen_messages_list = []
        for message in unseen_messages:
            message.display = MainProfile.objects.get(user=message.sender).display_name
            try:
                message.image = UserProfile.objects.get(user=message.sender).profile_image
            except UserProfile.DoesNotExist:
                message.image = "none"
            unseen_messages_list.append(message)

        # Check if the renewal date is expired and calculate days left
        renewal_message = 0
        days_left_for_renewal = 0
        try:
            if profile.renewal_due_date:
                current_date = timezone.now().date()
                renewal_date = profile.renewal_due_date
                
                print(current_date, renewal_date)

                if current_date > renewal_date:
                    renewal_message = 1  # Indicates expired renewal
                    days_left_for_renewal = (renewal_date - current_date).days  # Negative value for expired
                else:
                    days_left_for_renewal = (renewal_date - current_date).days  # Positive value for remaining days
            else:
                days_left_for_renewal = None  # If renewal date is missing, return None
        except AttributeError:  # Catch errors only when profile is None or missing attributes
            days_left_for_renewal = None
        
        try:
            main_profile = MainProfile.objects.get(user=current_user)
            main_profile = 1
        except MainProfile.DoesNotExist:
            main_profile = 0
        
        try:
            bio = Bio.objects.get(user=current_user)
            bio = 1
        except Bio.DoesNotExist:
            bio = 0

        print(renewal_message, days_left_for_renewal)

        is_admin = request.user.is_superuser or request.user.is_staff

        context.update({
            'usr_profile': profile,
            'usr_name': usr_name,
            'unseen_messages_count': unseen_messages_count,
            'unseen_messages': unseen_messages_list,
            'renewal_message': renewal_message,  # Add renewal message to context
            'days_left_for_renewal': days_left_for_renewal,  # Add days left to context
            'usr_img':usr_img,
            'main_profile': main_profile,
            'bio': bio,
            'is_admin': 1 if is_admin else 0
        })
    else:

        context.update({
            'usr_name': "No name",
            'unseen_messages_count': 0,
            'unseen_messages': [], 
            'renewal_message': 0,  # No renewal message for unauthenticated users
            'days_left_for_renewal': 0,  # No days left calculation for unauthenticated users
            'usr_img': 'none',
            'main_profile': None,
            'bio': None,
            'is_admin': is_admin
        })

    return context