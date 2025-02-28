from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

class OTPVerification(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    otp_key = models.CharField(max_length=6)  # Adjust the max_length as needed
    updated_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"OTPVerification(id={self.id}, otp_key={self.otp_key}, updated_time={self.updated_time})"

class ChapterName(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter_name = models.CharField(max_length=255)
    last_updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.chapter_name

class Industry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    last_updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Industries"

class Classification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    last_updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class MainProfile(models.Model):
    TITLE_CHOICES = [
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Miss', 'Miss'),
        ('Ms.', 'Ms.'),
        ('Dr.', 'Dr.'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    MEMBERSHIP_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Not Active', 'Not Active'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=5, choices=TITLE_CHOICES, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    suffix = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    product_service_description = models.CharField(max_length=255, blank=True, null=True)
    gst_registered_state = models.CharField(max_length=100, blank=True, null=True)
    gst_identification_number_or_pan = models.CharField(max_length=255, blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, blank=True, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, blank=True, null=True)
    requested_speciality = models.CharField(max_length=255, blank=True, null=True)
    membership_status = models.CharField(max_length=11, choices=MEMBERSHIP_STATUS_CHOICES)
    renewal_due_date = models.DateField(blank=True, null=True)
    active_until = models.DateField(blank=True, null=True)
    Chapter = models.ForeignKey('ChapterName', related_name='members', on_delete=models.SET_NULL, blank=True, null=True)
    my_business = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    sponsor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        unique=False,
        related_name='mainprofile_sponsor'
    )
    joining_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # If instance is being created
            self.joining_date = timezone.now().date()  # Assign current date to joining_date
        super(MainProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"


class ContactDetails(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    show_on_bni_public_websites = models.BooleanField(default=False)
    billing_address_quick_copy = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    direct_number = models.CharField(max_length=20, blank=True, null=True)
    home = models.CharField(max_length=20, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    pager = models.CharField(max_length=20, blank=True, null=True)
    voice_mail = models.CharField(max_length=20, blank=True, null=True)
    toll_free = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255)
    receive_updates_from_bni = models.BooleanField(default=False)
    share_revenue_data_with_bni_director = models.BooleanField(default=False)
    website = models.URLField(max_length=200, blank=True, null=True)
    social_networking_links = models.CharField(max_length=200, blank=True, null=True)

class Address(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=False)
    ADDRESS_CHOICES = [
        ('Main Address', 'Main Address'),
        ('Billing', 'Billing'),
        ('None', 'None'),
    ]
    should_appear = models.BooleanField(default=False)
    address_type = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    
class BillingAddress(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=False)
    ADDRESS_CHOICES = [
        ('Main Address', 'Main Address'),
        ('Billing', 'Billing'),
        ('None', 'None'),
    ]
    should_appear = models.BooleanField(default=False)
    address_line_1 = models.CharField(max_length=255) 
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

class Billing(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    same_as_above = models.BooleanField(default=False)
    billing_address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    billing_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_state = models.CharField(max_length=100, blank=True, null=True)
    billing_country = models.CharField(max_length=100, blank=True, null=True)
    billing_zip_code = models.CharField(max_length=20, blank=True, null=True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Bio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    years_in_business = models.PositiveIntegerField(blank=True, null=True)
    previous_jobs = models.TextField(blank=True)
    spouse = models.CharField(max_length=100, blank=True)
    children = models.CharField(max_length=100, blank=True)
    pets = models.CharField(max_length=100, blank=True)
    hobbies_and_interests = models.TextField(blank=True, null=True)
    city_of_residence = models.CharField(max_length=100, blank=True)
    years_in_city = models.PositiveIntegerField(blank=True, null=True)
    burning_desire = models.TextField(blank=True, null=True)
    something_no_one_knows = models.TextField(blank=True)
    key_to_success = models.TextField(blank=True)

    def __str__(self):
        return f'Bio for {self.user.username}'

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Connection(models.Model):
    user = models.ForeignKey(User, related_name='connections', on_delete=models.CASCADE)
    connection = models.ForeignKey(User, related_name='connected_to', on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('user', 'connection')


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f'From {self.sender} to {self.receiver}: {self.content}'

    def mark_as_seen(self):
        self.seen = True
        self.save()
        
class Testimonial(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    testimonials = models.TextField()
    from_user = models.ForeignKey(User, related_name='given_testimonials', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_testimonials', on_delete=models.CASCADE)
    TESTIMONIAL_CHOICES = [
        ('give_testimonials', 'Give Testimonials'),
        ('ask_testimonials', 'Ask Testimonials'),
    ]
    type = models.CharField(max_length=20, choices=TESTIMONIAL_CHOICES)
    updated_date = models.DateTimeField(auto_now=True)
    STATE_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    state_of_request = models.CharField(max_length=20, choices=STATE_CHOICES, default='pending')

    def __str__(self):
        return f'Testimonial from {self.from_user} to {self.to_user}'


class AccountSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_settings')
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Member to Member  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    BIO_VISIBILITY_CHOICES = [
        ('all', 'All'),
        ('connections', 'My Connections'),
        ('none', 'None'),
    ]
    bio_visibility = models.CharField(max_length=12, choices=BIO_VISIBILITY_CHOICES, default='all')
    connections_visibility = models.CharField(max_length=12, choices=BIO_VISIBILITY_CHOICES, default='all')
    testimonials_visibility = models.CharField(max_length=12, choices=BIO_VISIBILITY_CHOICES, default='all')
    gallery_visibility = models.CharField(max_length=12, choices=BIO_VISIBILITY_CHOICES, default='all')
    email_visibility = models.CharField(max_length=12, choices=BIO_VISIBILITY_CHOICES, default='all')
    contact_details_visibility = models.CharField(max_length=12, choices=BIO_VISIBILITY_CHOICES, default='all')
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Group Post Email Notifications>>>>>>>>>>>>>
    POST_NOTIFICATION_CHOICES = [
        ('every_time', 'Every time a new post is added'),
        ('daily', 'Once per day (daily digest)'),
        ('weekly', 'Once per week (weekly digest)'),
        ('never', 'Do not email me'),
    ]
    post_notifications = models.CharField(max_length=10, choices=POST_NOTIFICATION_CHOICES, default='every_time')
    
    #>>>>>>>>>>>>>>> Email Forwarding  >>>>>>>>>>>>>>>>>>>>>>>>
    #----------------------- Alternate notification email address-----------------------
    alternate_email = models.EmailField(blank=True, null=True)
    #-----------------------------------------------------------------------------------
    forward_messages = models.BooleanField(default=False)
    forward_sent_mail = models.BooleanField(default=False)
    forward_connection_requests = models.BooleanField(default=False)
    forward_recommendation_requests = models.BooleanField(default=False)
    country_settings_for_group_notifications = models.CharField(max_length=50, default='Default')

    def __str__(self):
        return f'Account Settings for {self.user}'


class WeeklyPresentation(models.Model):
    title = models.CharField(max_length=255)
    presentation_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_presentations')
    def __str__(self):
        return f'{self.title} on {self.presentation_date} by {self.user}'
        
class GAINSProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gains_profile')
    goals = models.TextField()
    accomplishments = models.TextField()
    interests = models.TextField()
    networks = models.TextField()
    skills = models.TextField()
    def __str__(self):
        return f'GAINS Profile for {self.user}'
        
class TopsProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tops_profile')
    ideal_referral = models.TextField()
    top_product = models.TextField()
    top_problem_solved = models.TextField()
    favourite_bni_story = models.TextField()
    ideal_referral_partner = models.TextField()
    def __str__(self):
        return f'Tops Profile for {self.user}'

class Gallery(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')
    last_updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if Gallery.objects.filter(user=self.user).count() >= 10:
            return 'You have reached the maximum number of uploads'
        else:
            super(Gallery, self).save(*args, **kwargs)

        def __str__(self):
            return f'Gallery Image - {self.user.username}'
        
############################################# Completely for admin dashboard ###############################################

class CountryData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country_name = models.CharField(max_length=255, unique=True)
    last_updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.country_name


class StateData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state_name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(
        CountryData, related_name='states', on_delete=models.CASCADE
    )
    last_updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.state_name


class CityData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city_name = models.CharField(max_length=255)
    country = models.ForeignKey(
        CountryData, related_name='cities', on_delete=models.CASCADE
    )  # Fixed reference
    state = models.ForeignKey(
        StateData, related_name='cities', on_delete=models.CASCADE
    )
    last_updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.city_name


class RegionPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    RegionpositionName = models.CharField(max_length=255)
    lastupdateddate = models.DateTimeField(auto_now=True)
    isRegion = models.BooleanField(default=False)

    def __str__(self):
        return self.RegionpositionName


class Region(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region_name = models.CharField(max_length=255)
    state = models.ForeignKey(
        StateData, related_name='regions', on_delete=models.CASCADE
    )
    country = models.ForeignKey(
        CountryData, related_name='regions', on_delete=models.CASCADE
    )
    city = models.ForeignKey(
        CityData, related_name='regions', on_delete=models.CASCADE
    )
    last_updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.region_name} in {self.city.city_name}, {self.country.country_name}'

class RegionMemberPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, related_name='member_positions', on_delete=models.CASCADE
    )
    position = models.ForeignKey(
        RegionPosition, related_name='member_positions', on_delete=models.CASCADE
    )
    region = models.ForeignKey(
        Region, related_name='member_positions', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user} - {self.position}'


class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.ForeignKey('ChapterName', related_name='chapters', on_delete=models.CASCADE)
    region = models.ForeignKey('Region', related_name='chapters', on_delete=models.CASCADE)
    country = models.ForeignKey('CountryData', related_name='chapters', on_delete=models.CASCADE)
    city = models.ForeignKey('CityData', related_name='chapters', on_delete=models.CASCADE)
    last_updated_date = models.DateField(auto_now=True)
    type = models.CharField(max_length=255, choices=[('online', 'Online'), ('offline', 'Offline')])
    day = models.CharField(
        max_length=9,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday')
        ]
    )
    chapter_members = models.ManyToManyField('MainProfile', related_name='chapters', blank=True)

    def __str__(self):
        return self.name.chapter_name  # Adjusted to display the ChapterName

class ChapterPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Chapterposition = models.CharField(max_length=255)
    is_chapter = models.BooleanField(default=False)
    lastupdateddate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Chapterposition

class ChapterMemberPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='chapter_member_positions', on_delete=models.CASCADE)
    position = models.ForeignKey(ChapterPosition, related_name='chapter_member_positions', on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name='chapter_member_positions', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.position}'
    
class Group(models.Model):
    OPEN = 'Open'
    INVITE_ONLY = 'Invite Only'
    VIEW_AND_POST = 'View and post'

    GROUP_TYPES = [
        (OPEN, 'Open'),
        (INVITE_ONLY, 'Invite Only'),
    ]

    ACCESS_TYPES = [
        (VIEW_AND_POST, 'View and post'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    group_type = models.CharField(max_length=20, choices=GROUP_TYPES)
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPES)
    language = models.CharField(max_length=100)  # This can be changed to a choice field if you have a predefined list of languages
    logo = models.ImageField(upload_to='group_logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    group_counts = models.PositiveIntegerField(default=0)
    lastupdateddate = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(User, related_name='joined_groups', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.members.filter(id=self.creator.id).exists():
            self.members.add(self.creator)

    def get_join_link(self):
        return reverse('join_group', args=[str(self.id)])

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

class TYFCB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tyfcb_created_by')
    thank_you_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tyfcb_thanked_to', null=True, blank=True)
    BUSINESS_TYPE_CHOICES = [
        ('new', 'New'),
        ('repeat', 'Repeat'),
    ]
    REFERRAL_TYPE_CHOICES = [
        ('tier_1', 'Tier 1'),
        ('tier_2', 'Tier 2'),
        ('tier_3+', 'Tier 3+'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter_name = models.ForeignKey(ChapterName, on_delete=models.CASCADE)
    region_name = models.ForeignKey(Region, on_delete=models.CASCADE)
    referral_amount = models.IntegerField()
    business_type = models.CharField(max_length=10, choices=BUSINESS_TYPE_CHOICES)
    referral_type = models.CharField(max_length=10, choices=REFERRAL_TYPE_CHOICES)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    comments = models.TextField()

    def __str__(self):
        return f"{self.chapter_name} - {self.region_name} - {self.referral_amount}"    

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class ReferralSlip(models.Model):
#     date = models.DateField(auto_now_add=True)
#     from_user = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE, 
#         related_name='referral_slips_created'  # Unique related_name for referrals created by the user
#     )
#     to_member = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE, 
#         related_name='referrals_received'  # Unique related_name for referrals received by the user
#     )
#     referral_description = models.TextField()
#     referral_type = models.CharField(max_length=20, choices=[('tier_1', 'Tier 1 (inside)'), ('tier_2', 'Tier 2 (outside)')])
#     referral_status = models.CharField(max_length=100, choices=[('given_card', 'Given your card'), ('will_call', 'Told them you would call')])
#     address = models.CharField(max_length=255, blank=True)
#     telephone = models.CharField(max_length=15)
#     email = models.EmailField(blank=True)
#     comments = models.TextField(blank=True)
#     referral_heat = models.CharField(max_length=10, choices=[('hot', 'Hot'), ('tepid', 'Tepid')])

class Meeting(models.Model):
    MEETING_TYPES = [
        ('one_to_one', 'One-to-One'),
        ('group', 'Group'),
    ]
    chapter = models.CharField(max_length=100, default='Radiance')
    met_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings_met_with')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings_invited_by')
    location = models.CharField(max_length=255)
    topics_of_conversation = models.TextField()
    date = models.DateField()
    meeting_type = models.CharField(max_length=10, choices=MEETING_TYPES, default='one_to_one')

    def __str__(self):
        return f"{self.get_meeting_type_display()} on {self.date} at {self.location}"



class ChapterEducationUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ceus')
    date = models.DateField(default=timezone.now)
    course_title = models.CharField(max_length=255)
    credits_per_course = models.DecimalField(max_digits=4, decimal_places=1)
    qty_earned = models.IntegerField(default=0)
    total_credits_last_week = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.course_title} ({self.date}) - {self.user.username}"

class ReferralSlip(models.Model):
    date = models.DateField(auto_now_add=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_slips_created')
    to_member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_received')
    referral_description = models.TextField()
    referral_type = models.CharField(max_length=20, choices=[('tier_1', 'Tier 1 (inside)'), ('tier_2', 'Tier 2 (outside)')])
    referral_status = models.CharField(max_length=100, choices=[('given_card', 'Given your card'), ('will_call', 'Told them you would call')])
    address = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    comments = models.TextField(blank=True)
    referral_heat = models.CharField(max_length=10, choices=[('hot', 'Hot'), ('tepid', 'Tepid')])
    updated_at = models.DateTimeField(auto_now=True)  # Add this field

    def __str__(self):
        return f"Referral from {self.from_user} to {self.to_member}"
    
class WeeklySlip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.CharField(max_length=255)
    run_at = models.DateTimeField(auto_now_add=True)
    from_date = models.DateField()
    to_date = models.DateField()
    referral_to = models.CharField(max_length=255)
    referral_from = models.CharField(max_length=255)
    referral = models.CharField(max_length=255)
    tyfcb = models.TextField()
    one_to_ones = models.TextField()
    visitors = models.TextField()

    def __str__(self):
        return f"Weekly Slip for {self.user.username} from {self.from_date} to {self.to_date}"


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'

    class Meta:
        ordering = ('timestamp',)
        
class oneToOneMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f'From {self.sender} to {self.receiver}: {self.content}'

    def mark_as_seen(self):
        self.seen = True
        self.save()

  
class ContactFormSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=2)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    
class Visitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state_country_province = models.CharField(max_length=50, blank=True, null=True)
    post_code = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=50)
    visitor_type = models.CharField(max_length=20)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class ChapterGoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    attendance_percentage = models.FloatField()
    total_number_of_1_to_1s = models.IntegerField()
    ceus = models.FloatField()
    visitors = models.IntegerField()
    new_memberships = models.IntegerField()
    number_of_members_in_chapter = models.IntegerField()
    number_of_referrals = models.IntegerField()
    thank_you_for_closed_business = models.FloatField()
    date_of_month = models.DateField()
    updated_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.chapter.name.chapter_name} Goals"

        
class TrainingSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training_name = models.CharField(max_length=255)
    date = models.DateField()
    last_updated_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.training_name} on {self.date}'
    
class TrainingSessionProfile(models.Model):
    user = models.ForeignKey(MainProfile, on_delete=models.CASCADE)
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    selected_date = models.DateField()
    updated_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.training_session.training_name} on {self.selected_date}'


class PAS(models.Model):
    user = models.ForeignKey(MainProfile, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    absent = models.BooleanField(default=False)
    updated_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.chapter.name.chapter_name} - {self.date}'
