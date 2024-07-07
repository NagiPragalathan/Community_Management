from django.shortcuts import render
from django.shortcuts import render, redirect
from base.models import CityData, Group, Connection, MainProfile, oneToOneMessage, UserProfile
from base.form.forms import CityDataForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User


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
            usr_image = UserProfile.objects.get(user=current_user).profile_image
        except:
            usr_image = "none"
        unseen_messages = oneToOneMessage.objects.filter(receiver=current_user, seen=False)
        unseen_messages_count = unseen_messages.count()

        # Annotate each message with the sender's display name
        unseen_messages_list = []
        for message in unseen_messages:
            message.display = MainProfile.objects.get(user=message.sender).display_name
            try:
                message.image = UserProfile.objects.get(user=message.sender).profile_image
            except:
                message.image = "none"
                
            unseen_messages_list.append(message)
            print(message)

        context.update({
            'usr_profile': profile,
            'usr_name': usr_name,
            'unseen_messages_count': unseen_messages_count,
            'unseen_messages': unseen_messages_list,
            'usr_image':usr_image
        })
    else:
        return redirect("login")

    return context

