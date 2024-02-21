# Django  inbuilt models
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from QuizApp import settings

# Django views
from base.views.auth import *
from base.views.common import *
from base.views.FileManagement import *
from base.views.Profile import *

from django.contrib.auth.views import PasswordResetConfirmView

urlpatterns = []

admin_ = [
    path('admin/', admin.site.urls),   
    path('admin/', admin.site.urls, name='admin'), 
]

auth = [
    path('accounts/', include('django.contrib.auth.urls')),  # Use built-in authentication views
    path('enter_otp', enter_otp, name='enter_otp'),
    path('signup/<str:mail>', signup, name='signup'),
    path('login', user_login, name='login'),
    path('change_password', change_password, name='change_password'),
    path('forgot_password', forgot_password, name='forgot_password'),
    path('logout', logout_view, name='logout'),
    path('reset/<uidb64>/<token>/', custom_password_reset_confirm, name='custom_password_reset_confirm'),
]

common = [
    path('home', home, name='home'),
    path('', home, name='home'),
]

file_manager = [
    path('add_data', add_data, name='add_data'),
    path('list_data', list_data, name='list_data'),
    path('add_folder', add_folder, name='add_folder'),
    path('list_folders/<str:path>', list_folders, name='list_folders'),
]

profile =[
    path('add_profile', add_profile, name='add_profile'),
    path('add_contact_details', add_contact_details, name='add_contact_details'),
]

urlpatterns.extend(auth)
urlpatterns.extend(admin_)
urlpatterns.extend(common)
urlpatterns.extend(profile)
urlpatterns.extend(file_manager)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

