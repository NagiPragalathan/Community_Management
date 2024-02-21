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
    social_networking_links = models.ManyToManyField('SocialNetworkingLink')

class Address(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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

class SocialNetworkingLink(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name