from django.shortcuts import render
from django.shortcuts import render, redirect
from base.models import CityData, Group, Connection, MainProfile, oneToOneMessage, UserProfile
from base.form.forms import CityDataForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone

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
    
    context = {
        'group_count': group_count,
        'connection_count': connection_count,
    }
    return render(request, 'dashboard.html', context)

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
        profile = MainProfile.objects.get(user=current_user)
        try:
            usr_img = UserProfile.objects.get(user=current_user).profile_image
        except:
            usr_img = "none"
        
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
        if profile.renewal_due_date:
            current_date = timezone.now().date()
            renewal_date = profile.renewal_due_date

            if current_date > renewal_date:
                renewal_message = 1
                days_left_for_renewal = (current_date - renewal_date).days * -1  # Negative days to indicate expiration
            else:
                days_left_for_renewal = (renewal_date - current_date).days

        context.update({
            'usr_profile': profile,
            'usr_name': usr_name,
            'unseen_messages_count': unseen_messages_count,
            'unseen_messages': unseen_messages_list,
            'renewal_message': renewal_message,  # Add renewal message to context
            'days_left_for_renewal': days_left_for_renewal,  # Add days left to context
            'usr_img':usr_img
        })
    else:
        context.update({
            'usr_name': "No name",
            'unseen_messages_count': 0,
            'unseen_messages': [],
            'renewal_message': 0,  # No renewal message for unauthenticated users
            'days_left_for_renewal': 0,  # No days left calculation for unauthenticated users
            'usr_img': 'none'
        })

    return context