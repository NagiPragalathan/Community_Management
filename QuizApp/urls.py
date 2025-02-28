# Django  inbuilt models
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from QuizApp import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import re_path

# Django views
from base.views.industry_clasification import *
from base.views.json_rep import download_user_data
from base.views.auth import *
from base.views.common import *
from base.views.Profile import *
from base.views.connections import *
from base.views.chat import *
from base.views.Testimonials import *
from base.views.GroupCURD import *
from base.views.AccountSettings import *
from base.views.pas import *
from base.views.training_operation import *
from base.views.tyfcb import *
from base.views.referrals import *
from base.views.onetoone import *
from base.views.ceu import *
from base.views.weeklyslips import *
from base.views.operations import *
from base.views.reports import *
from base.views.contact import *
from base.views.training import *
from base.admin_views.region.region import *
from base.admin_views.region.country_data import *
from base.admin_views.region.state_data import *
from base.admin_views.region.city_data import *
from base.admin_views.region.region_position import *
from base.admin_views.region.region_member_position import *
from base.admin_views.chapter.chapter_name import *
from base.admin_views.chapter.chapter_position import *
from base.admin_views.chapter.chapter_member_positions import *
from base.admin_views.chapter.chapter import *
from base.admin_views.chapter.profile import *

from base.views.reports_collection.chapter_meeting_report import *
from base.views.reports_collection.member_performance_report import *
from base.views.reports_collection.chapter_performance_report import *
from base.views.reports_collection.region_performance_report import *
from base.views.reports_collection.chapter_roster_report import *
from base.views.reports_collection.training_sessions_report import *

from django.contrib.auth.views import PasswordResetConfirmView

urlpatterns = []

common = [
    path('admin/', admin.site.urls, name='django_admin'),
    path('dashboard/', dashboard, name='dashboard'),
    path('chart_dashboard', chart_dashboard, name='chart_dashboard'),
    path('', index, name='index'),
    path('add_city', add_city, name="add_city")
]

external_url = [
    path('select2/', include('django_select2.urls')),
]


auth = [
    path('accounts/', include('django.contrib.auth.urls')),  # Use built-in authentication views
    path('enter_otp', enter_otp, name='enter_otp'),
    # path('signup/<str:mail>', signup, name='signup'),
    path('signup', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('change_password', change_password, name='change_password'),
    path('forgot_password', forgot_password, name='forgot_password'),
    path('logout', logout_view, name='logout'),
    path('reset/<uidb64>/<token>/', custom_password_reset_confirm, name='custom_password_reset_confirm'),
]


profile =[
    path('profile/profile_management/<str:username>', profile_management, name='profile_management'),
    path('add_edit_user_profile', add_edit_user_profile, name='add_edit_user_profile'), # here we can create new user so this is first tab.
    path('add_profile/<str:username>', add_profile, name='add_profile'),
    path('add_profile/<str:username>/<int:dashboard>', add_profile, name='add_profile'),
    path('add_contact_details/<str:username>', add_contact_details, name='add_contact_details'),
    path('add_contact_details/<str:username>/<int:dashboard>', add_contact_details, name='add_contact_details'),
    path('add_or_edit_address/<str:username>', add_or_edit_address, name='add_or_edit_address'),
    path('add_or_edit_address/<str:username>/<int:dashboard>', add_or_edit_address, name='add_or_edit_address'),
    path('add_or_edit_bio/<str:username>', add_or_edit_bio, name='add_or_edit_bio'),
    path('add_or_edit_bio/<str:username>/<int:dashboard>', add_or_edit_bio, name='add_or_edit_bio'),
    path('delete_image', delete_image, name='delete_image'),
    path('add_gallery', add_gallery, name='add_gallery'),

]

connections = [ 
    path('send_connection_request/<int:user_id>', send_connection_request, name='send_connection_request'),
    path('accept_connection_request/<int:connection_id>', accept_connection_request, name='accept_connection_request'),
    path('connections', connection_list, name='connections'),
    path('connections/<str:username>', connection_list, name='connections'),
    path('list_users', list_users, name='list_users'),
    path('pending_request', pending_request, name='pending_request'),
    path('incoming_requests', incoming_requests, name='incoming_requests'),
    path('reject_connection_request/<int:connection_id>', reject_connection_request, name='reject_connection_request'),
]

chat = [
    path('chat/<int:receiver_id>/', chat_view, name='chat'),
    path('update_message/<int:receiver_id>/', update_message, name='update_message'),
    path('get_messages/<int:receiver_id>/', one_to_one_get_messages, name='get_messages'),
    path('unseen_messages', unseen_messages, name='unseen_messages'),
]

testimonial = [
    path('menuOfTestimonial', menuOfTestimonial, name='menuOfTestimonial'),
    path('incoming_testimonials', incoming_testimonials, name='incoming_testimonials'),
    path('incoming_testimonials/<str:username>', incoming_testimonials, name='incoming_testimonials'),
    path('list_requested_testimonials', list_requested_testimonials, name='list_requested_testimonials'),
    path('list_inboxrequested_testimonials', list_inboxrequested_testimonials, name='list_inboxrequested_testimonials'),
    path('give_testimonial/<int:receiver_id>', give_testimonial, name='give_testimonial'),
    path('request_testimonial/<int:receiver_id>', request_testimonial, name='request_testimonial'),
]

account_settings = [
    path('edit_or_add_account_settings', edit_or_add_account_settings, name='edit_or_add_account_settings'),
    path('edit_or_add_account_settings/<str:username>', edit_or_add_account_settings, name='edit_or_add_account_settings'),
    path('edit_or_add_account_settings/<str:username>/<int:dashboard>', edit_or_add_account_settings, name='edit_or_add_account_settings'),
]



tyfcb = [
    path('tyfcb/', tyfcb_list, name='tyfcb_list'),
    path('tyfcb/new/', tyfcb_create, name='tyfcb_create'),
    path('tyfcb/<uuid:pk>/', tyfcb_detail, name='tyfcb_detail'),
    path('tyfcb/<uuid:pk>/edit/', tyfcb_edit, name='tyfcb_edit'),
    path('tyfcb/<uuid:pk>/delete/', tyfcb_delete, name='tyfcb_delete'),
]

referrals = [
    path('referrals/new/', create_referral, name='create_referral'),
    path('referrals/', list_referrals, name='list_referrals'),
    path('referral-report/', referral_report, name='referral_report'), 

]

onetoone =[
    path('meetings/new/', create_meeting, name='create_meeting'),
    path('meetings/', meeting_list, name='meeting_list'),
    path('meetings/one-to-one/', one_to_one_list, name='one_to_one_list'),
    path('meetings/<int:meeting_id>/edit/', edit_meeting, name='edit_meeting'),
    path('meetings/<int:meeting_id>/delete/', delete_meeting, name='delete_meeting'),
]

ceu = [
    path('ceus/create/', create_ceu, name='create_ceu'),
    path('ceus/review/', review_ceu, name='review_ceu'),
    path('ceus/<int:ceu_id>/edit/', edit_ceu, name='edit_ceu'),
    path('ceus/<int:ceu_id>/delete/', delete_ceu, name='delete_ceu'),
]

weeklyslips =[
    path('weeklyslips/weeklyslips/', weekly_slips, name='weekly_slips'),
]


group_chat = [
    path('chat/<str:room_name>/', room, name='room'),
    path('chat/<str:room_name>/send/', send_message, name='send_message'),
    path('chat/<str:room_name>/messages/', get_messages, name='get_messages'),
]

group = [
    path('groups/', list_groups, name='list_groups'),
    path('mygroups/', my_list_groups, name='my_list_groups'),
    path('joined_groups/', joined_groups, name='joined_groups'),
    path('groups/new/', group_crud, name='group_crud_new'),
    path('groups/<uuid:pk>/', group_crud, name='group_crud'),
    path('join/<uuid:group_id>/', join_group, name='join_group'),
]

visitor = [
    # path('register/', register_visitor, name='register_visitor'),
    path('visitors/', visitor_registration_portal, name='visitor_registration_portal'),
    path('visitors/register/', register_visitor, name='register_visitor'),
    path('visitors/<int:visitor_id>/edit/', register_visitor, name='edit_visitor'),
    path('visitors/<int:visitor_id>/delete/', delete_visitor, name='delete_visitor'),
    
    path('subscription-expired/', subscription_expired, name='subscription_expired'),
]

Operations = [
    path('view_palms_summary/', view_palms_summary, name='view_palms_summary'),
    path('view_chapter_goals/', view_chapter_goals, name='view_chapter_goals'),
    path('email_my_chapter/', email_my_chapter, name='email_my_chapter'),
    path('email_visitor_invitation/', email_visitor_invitation, name='email_visitor_invitation'),
    path('email_chapter_visitors/', email_chapter_visitors, name='email_chapter_visitors'),
    path('manage_news/', manage_news, name='manage_news'),
    path('operations/operations', operations, name='operations'),
    path('user_chapter_emails', user_chapter_emails, name='user_chapter_emails'),
    
    # Add other URL configurations
]

contact = [
    
    path('contact', contact_form, name='contact_form'),

]

goals = [
    path('set_goals', set_goals, name='set_goals'),
    path('goals_list', goals_list, name='goals_list'),
]

reports_url = [
    # path('training_sessions/',training_session_list, name='training_session_list'),
    # path('add_training_session/',add_training_session, name='add_training_session'),
    # path('get_chapter_users/',get_chapter_users, name='get_chapter_users'),
]

# start custom admin

admin_region = [
    path("regions/", region_list, name="region_list"),
    path("regions/create/", create_region, name="create_region"),
    path("regions/<uuid:region_id>/update/", update_region, name="update_region"),  # Updated to <uuid:region_id>
    path("regions/<uuid:region_id>/delete/", delete_region, name="delete_region"),  # Updated to <uuid:region_id>
]

admin_country = [
    path('country/', country_list, name='country_list'),
    path('country/create/', country_create, name='country_create'),
    path('country/edit/<uuid:pk>/', country_edit, name='country_edit'),
    path('country/delete/<uuid:pk>/', country_delete, name='country_delete'),
]

admin_state = [
    path('states/', state_list, name='state_list'),  # List all states
    path('states/create/', state_create, name='state_create'),  # Create a state
    path('states/edit/<uuid:state_id>/', state_edit, name='state_edit'),  # Edit a state
    path('states/delete/<uuid:state_id>/', state_delete, name='state_delete'),  # Delete a state
]

admin_city = [
    path('cities/', city_list, name='city_list'),
    path('cities/create/', city_create, name='city_create'),
    path('cities/edit/<uuid:city_id>/', city_edit, name='city_edit'),  
    path('cities/delete/<uuid:city_id>/', city_delete, name='city_delete'),
]

admin_region_position = [
    path('region_positions/', list_region_positions, name='list_region_positions'),
    path('region_positions/create/', create_region_position, name='create_region_position'),
    path('region_positions/edit/<uuid:id>/', edit_region_position, name='edit_region_position'),
    path('region_positions/delete/<uuid:id>/', delete_region_position, name='delete_region_position'),
]

admin_region_member_position = [
    path('region_member_positions/', region_member_position_list, name='region_member_position_list'),
    path('region_member_positions/create/', region_member_position_create, name='region_member_position_create'),
    path('region_member_positions/edit/<uuid:id>/', region_member_position_edit, name='region_member_position_edit'),
    path('region_member_positions/delete/<uuid:id>/', region_member_position_delete, name='region_member_position_delete'),
]

# chapter Urls

admin_chapter_name = [
    path('chapter_name/', chapter_name_list, name='chapter_name_list'),
    path('chapter_name/create/', chapter_name_create, name='chapter_name_create'),
    path('chapter_name/edit/<uuid:pk>/', chapter_name_edit, name='chapter_name_edit'),
    path('chapter_name/delete/<uuid:pk>/', chapter_name_delete, name='chapter_name_delete'),
]

admin_chapter_position = [
    path('chapter_position/', chapter_position_list, name='chapter_position_list'),
    path('chapter_position/create/', chapter_position_create, name='chapter_position_create'),
    path('chapter_position/edit/<uuid:pk>/', chapter_position_edit, name='chapter_position_edit'),
    path('chapter_position/delete/<uuid:pk>/', chapter_position_delete, name='chapter_position_delete'),
]


admin_chapter_member_position = [
    path('chapter_member_positions/', list_chapter_member_positions, name='list_chapter_member_positions'),
    path('chapter_member_positions/create/', create_chapter_member_position, name='create_chapter_member_position'),
    path('chapter_member_positions/edit/<uuid:id>/', edit_chapter_member_position, name='edit_chapter_member_position'),
    path('chapter_member_positions/delete/<uuid:id>/', delete_chapter_member_position, name='delete_chapter_member_position'),
]

admin_chapter = [
    path('chapter/', chapter_list, name='chapter_list'),
    path('chapter/create/', chapter_create, name='chapter_create'),
    path('chapter/<uuid:pk>/edit/', chapter_edit, name='chapter_edit'),
    path('chapter/<uuid:pk>/delete/', chapter_delete, name='chapter_delete'),
]

admin_profile = [
    # URL for creating a new profile
    path('profile/create/', profile_view, name='profile-create'),
    path('profile/list/', profile_list_view, name='profile-list'),
    path('profile-view/username-list/', username_list_view, name='username-list'),
    # URL for editing an existing profile
    path('profile/edit/<int:pk>/', profile_view, name='profile-edit'),
    path('profile/<str:username>/', view_profile, name='view_profile'),
]

training_sessions = [
    path('training_sessions/', list_training_sessions, name='list_training_sessions'),
    path('training_sessions/create/', create_training_session, name='create_training_session'),
    path('training_sessions/edit/<uuid:pk>/', edit_training_session, name='edit_training_session'),
    path('training_sessions/delete/<uuid:pk>/', delete_training_session, name='delete_training_session'),
    
    path('chapter-profiles/', chapter_profiles_view, name='chapter_profiles'),
    path('edit_training_session/', edit_training_session_view, name='edit_training_session'),
]

pas = [
    path('chapter-members/', chapter_members, name='chapter_members'),
    path('update-attendance/', update_attendance, name='update_attendance'),
]

member_performance_report_url = [
    path('member-performance-report/', member_performance_report, name='member_performance_report'),
]

chapter_meeting_report_url = [
    path('chapter-meeting-report/', chapter_meeting_report, name='chapter_meeting_report'),
]

chapter_performance_report_url = [
    path('chapter-performance-report/', chapter_performance_report, name='chapter_performance_report'),
]

region_performance_report_url = [
    path('region-performance-report/', region_performance_report, name='region_performance_report'),
]

chapter_roster_report_url = [
    path('chapter-roster-report/', chapter_roster_report, name='chapter_roster_report'),
]

training_sessions_report_url = [
    path('training-sessions-report/', training_sessions_report, name='training_sessions_report'),
]

iframe_url = [
    path('iframe/<str:username>/', iframe, name='iframe'),
    path('iframe/<str:username>/<int:dashboard>', iframe, name='iframe'),
    path('email/', email, name='email'),
    path('portal/', portal, name='portal'),
]

download_data = [
    path('download-data/<str:username>/', download_user_data, name='download_user_data'),
]

industry_classification = [
    # Industry URLs
    path('industries/', industry_list, name='industry_list'),
    path('industry/<uuid:pk>/', industry_detail, name='industry_detail'),
    path('industry/new/', industry_create, name='industry_create'),
    path('industry/<uuid:pk>/edit/', industry_update, name='industry_update'),
    path('industry/<uuid:pk>/delete/', industry_delete, name='industry_delete'),

    # Classification URLs
    path('classifications/', classification_list, name='classification_list'),
    path('classification/<uuid:pk>/', classification_detail, name='classification_detail'),
    path('classification/new/', classification_create, name='classification_create'),
    path('classification/<uuid:pk>/edit/', classification_update, name='classification_update'),
    path('classification/<uuid:pk>/delete/', classification_delete, name='classification_delete'),
]


urlpatterns.extend(auth)
urlpatterns.extend(chat)
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
urlpatterns+=pas
urlpatterns+=external_url
urlpatterns+=group_chat
urlpatterns+=visitor
urlpatterns+=contact
urlpatterns+=Operations
urlpatterns+=goals
urlpatterns+=reports_url
urlpatterns+=admin_region
urlpatterns+=admin_country
urlpatterns+=admin_state
urlpatterns+=admin_city
urlpatterns+=admin_region_position
urlpatterns+=admin_region_member_position
urlpatterns+=admin_chapter_name
urlpatterns+=admin_chapter_position
urlpatterns+=admin_chapter_member_position
urlpatterns+=admin_chapter
urlpatterns+=admin_profile
urlpatterns+=training_sessions
urlpatterns+=industry_classification

# reports
urlpatterns+=member_performance_report_url
urlpatterns+=chapter_meeting_report_url
urlpatterns+=chapter_performance_report_url
urlpatterns+=region_performance_report_url
urlpatterns+=chapter_roster_report_url
urlpatterns+=training_sessions_report_url
urlpatterns+=iframe_url

# download data
urlpatterns+=download_data

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
