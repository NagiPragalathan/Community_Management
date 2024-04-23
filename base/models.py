from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class OTPVerification(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    otp_key = models.CharField(max_length=6)  # Adjust the max_length as needed
    updated_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"OTPVerification(id={self.id}, otp_key={self.otp_key}, updated_time={self.updated_time})"
    
class PathManager(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.CharField(max_length=400)  # Adjust max_length as needed
    file = models.FileField(upload_to='Files/')  # Adjust upload_to as needed
    category = models.CharField(max_length=50)  # Adjust max_length as needed
    title = models.CharField(max_length=255)  # Adjust max_length as needed
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.user_id.username}'
    
class FolderManager(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    FolderName = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    path = models.CharField(max_length=400)
    updated_date = models.DateTimeField(auto_now=True)


class MainProfile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=5, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    suffix = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=6)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    product_service_description = models.CharField(max_length=255, blank=True, null=True)
    gst_registered_state = models.CharField(max_length=100, blank=True, null=True)
    gst_identification_number_or_pan = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    classification = models.CharField(max_length=255, blank=True, null=True)
    requested_speciality = models.CharField(max_length=255, blank=True, null=True)
    membership_status = models.CharField(max_length=11)
    RenewalDueDate = models.CharField(max_length=255, blank=True, null=True) # dynamic
    Chapter = models.CharField(max_length=255, blank=True, null=True) # dynamic
    my_business = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

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

