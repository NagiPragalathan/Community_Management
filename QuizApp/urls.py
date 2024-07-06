# Django  inbuilt models
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from QuizApp import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import re_path

# Django views
from base.views.auth import *
from base.views.common import *
from base.views.Profile import *
from base.views.connections import *
from base.views.chat import *
from base.views.Testimonials import *
from base.views.GroupCURD import *
from base.views.AccountSettings import *
from base.views.tyfcb import *
from base.views.referrals import *
<<<<<<< HEAD
from base.views.consumers import *
=======
from base.views.onetoone import *
from base.views.ceu import *
from base.views.weeklyslips import *

>>>>>>> fb90d919f1f8ab98742a380b1e2b279258119e99


from django.contrib.auth.views import PasswordResetConfirmView

urlpatterns = []



common = [
    path('dashboard', dashboard, name='dashboard'),
    path('', index, name='index'),
    path('add_city', add_city, name="add_city")
]


admin_ = [
    path('admin/', admin.site.urls, name='admin'),
]

admin_ += i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
)

auth = [
    path('accounts/', include('django.contrib.auth.urls')),  # Use built-in authentication views
    path('enter_otp', enter_otp, name='enter_otp'),
    # path('signup/<str:mail>', signup, name='signup'),
    path('signup', signup, name='signup'),
    path('login', user_login, name='login'),
    path('change_password', change_password, name='change_password'),
    path('forgot_password', forgot_password, name='forgot_password'),
    path('logout', logout_view, name='logout'),
    path('reset/<uidb64>/<token>/', custom_password_reset_confirm, name='custom_password_reset_confirm'),
]


profile =[
    path('add_profile', add_profile, name='add_profile'),
    path('add_contact_details', add_contact_details, name='add_contact_details'),
    path('add_edit_user_profile', add_edit_user_profile, name='add_edit_user_profile'),
    path('add_or_edit_address', add_or_edit_address, name='add_or_edit_address'),
    path('add_or_edit_bio', add_or_edit_bio, name='add_or_edit_bio'),
    path('delete_image', delete_image, name='delete_image'),
    path('add_gallery', add_gallery, name='add_gallery'),
]

connections = [ 
    path('send_connection_request/<int:user_id>', send_connection_request, name='send_connection_request'),
    path('accept_connection_request/<int:connection_id>', accept_connection_request, name='accept_connection_request'),
    path('connections', connection_list, name='connection_list'),
    path('list_users', list_users, name='list_users'),
    path('incoming_requests', incoming_requests, name='incoming_requests'),
    path('reject_connection_request/<int:connection_id>', reject_connection_request, name='reject_connection_request'),
    path('accept_connection_request/<int:connection_id>', accept_connection_request, name='accept_connection_request'),
]

chat = [
    path('chat/<int:receiver_id>/', chat_view, name='chat'),
    path('update_message/<int:receiver_id>/', update_message, name='update_message'),
    path('get_messages/<int:receiver_id>/', get_messages, name='get_messages'),
    path('unseen_messages', unseen_messages, name='unseen_messages'),
]

testimonial = [
    path('incoming_testimonials', incoming_testimonials, name='incoming_testimonials'),
    path('list_requested_testimonials', list_requested_testimonials, name='list_requested_testimonials'),
    path('list_inboxrequested_testimonials', list_inboxrequested_testimonials, name='list_inboxrequested_testimonials'),
    path('give_testimonial/<int:receiver_id>', give_testimonial, name='give_testimonial'),
    path('request_testimonial/<int:receiver_id>', request_testimonial, name='request_testimonial'),
]

account_settings = [
    path('edit_or_add_account_settings', edit_or_add_account_settings, name='edit_or_add_account_settings'),
]

group = [
    path('groups/', list_groups, name='list_groups'),
    path('groups/new/', group_crud, name='group_crud_new'),
    path('groups/<uuid:pk>/', group_crud, name='group_crud'),
    path('select2/', include('django_select2.urls')),
    path('chat/<str:room_name>/', room, name='room'),
]

tyfcb =[
    path('tyfcb/', tyfcb_list, name='tyfcb_list'),
    path('tyfcb_review/', tyfcb_list, name='tyfcb_review'),
    path('tyfcb/new/', tyfcb_create, name='tyfcb_create'),
    path('tyfcb/<uuid:pk>/', tyfcb_detail, name='tyfcb_detail'),
    path('tyfcb/<uuid:pk>/edit/', tyfcb_edit, name='tyfcb_edit'),
]

referrals = [
    path('referrals/new/', create_referral, name='create_referral'),
    path('referrals/', list_referrals, name='list_referrals'),
    path('referral-report/', referral_report, name='referral_report'), 

]

<<<<<<< HEAD
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]

=======
onetoone =[
    path('meetings/new/', create_meeting, name='create_meeting'),
    path('meetings/', meeting_list, name='meeting_list'),
    path('meetings/one-to-one/', one_to_one_list, name='one_to_one_list'),
]

ceu =[
    path('ceus/create/', create_ceu, name='create_ceu'),
    path('ceus/review/', review_ceu, name='review_ceu'),
]

weeklyslips =[
    path('weeklyslips/weeklyslips/', weekly_slips, name='weekly_slips'),
]


>>>>>>> fb90d919f1f8ab98742a380b1e2b279258119e99

urlpatterns.extend(auth)
urlpatterns.extend(chat)
urlpatterns.extend(admin_)
urlpatterns.extend(group)
urlpatterns.extend(common)
urlpatterns.extend(profile)
urlpatterns.extend(testimonial)
urlpatterns.extend(connections)
urlpatterns.extend(account_settings)
urlpatterns.extend(tyfcb)
urlpatterns.extend(referrals)
urlpatterns.extend(onetoone)
urlpatterns.extend(weeklyslips)
urlpatterns+=ceu

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
