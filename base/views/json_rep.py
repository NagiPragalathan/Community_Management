from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from base.models import (MainProfile, ContactDetails, Address, BillingAddress, UserProfile, 
                    Bio, Connection, Testimonial, AccountSettings, WeeklyPresentation, 
                    GAINSProfile, TopsProfile, Gallery, TYFCB, Meeting, ChapterEducationUnit, 
                    ReferralSlip, WeeklySlip, Visitor, ChapterGoles, TrainingSessionProfile, PAS)
from django.core.serializers import serialize
import json
from django.contrib.auth.decorators import login_required
import uuid
from django.db.models.fields.files import ImageFieldFile

@login_required
def download_user_data(request, username):
    """Download all data associated with a user as JSON"""
    user = get_object_or_404(User, username=username)
    
    # Create a dictionary to store all user data
    user_data = {
        'user': {
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
        }
    }

    # Helper function to safely get related model data
    def get_model_data(model, filter_kwargs):
        try:
            instance = model.objects.filter(**filter_kwargs).first()
            if instance:
                return {field.name: getattr(instance, field.name) 
                        for field in model._meta.fields 
                        if not field.is_relation}
        except model.DoesNotExist:
            pass
        return None

    # Helper function to safely get related model list data
    def get_model_list_data(model, filter_kwargs):
        instances = model.objects.filter(**filter_kwargs)
        return [{field.name: getattr(instance, field.name) 
                for field in model._meta.fields 
                if not field.is_relation}
                for instance in instances]

    # Collect data from related models
    related_data = {
        'main_profile': get_model_data(MainProfile, {'user': user}),
        'contact_details': get_model_data(ContactDetails, {'user': user}),
        'address': get_model_data(Address, {'user': user}),
        'billing_address': get_model_data(BillingAddress, {'user': user}),
        'user_profile': get_model_data(UserProfile, {'user': user}),
        'bio': get_model_data(Bio, {'user': user}),
        'account_settings': get_model_data(AccountSettings, {'user': user}),
        'gains_profile': get_model_data(GAINSProfile, {'user': user}),
        'tops_profile': get_model_data(TopsProfile, {'user': user}),
        
        # Lists of related data
        'connections': get_model_list_data(Connection, {'user': user}),
        'testimonials_given': get_model_list_data(Testimonial, {'from_user': user}),
        'testimonials_received': get_model_list_data(Testimonial, {'to_user': user}),
        'weekly_presentations': get_model_list_data(WeeklyPresentation, {'user': user}),
        'gallery': get_model_list_data(Gallery, {'user': user}),
        'tyfcb': get_model_list_data(TYFCB, {'user': user}),
        'meetings': get_model_list_data(Meeting, {'invited_by': user}),
        'ceus': get_model_list_data(ChapterEducationUnit, {'user': user}),
        'referral_slips': get_model_list_data(ReferralSlip, {'from_user': user}),
        'weekly_slips': get_model_list_data(WeeklySlip, {'user': user}),
        'visitors': get_model_list_data(Visitor, {'user': user}),
        'chapter_goals': get_model_list_data(ChapterGoles, {'user': user}),
        'training_sessions': get_model_list_data(TrainingSessionProfile, {'user__user': user}),
        'pas': get_model_list_data(PAS, {'user__user': user}),
    }

    # Add related data to user_data
    user_data.update(related_data)

    # Convert datetime objects, UUIDs, and ImageFields to strings
    def datetime_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, ImageFieldFile):
            return str(obj.url) if obj else None
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    # Create the response with the JSON data
    response = JsonResponse(user_data, json_dumps_params={'default': datetime_handler})
    response['Content-Disposition'] = f'attachment; filename="{username}_data.json"'
    return response 