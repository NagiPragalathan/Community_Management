from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        expected_paths = [
            reverse('login'),
            reverse('index'),
            reverse('contact_form'),
        ]
        # Check if the user is not authenticated and the request is not for the login page
        if not request.user.is_authenticated and request.path not in expected_paths:
            return redirect('login')  # Redirect to the login page
        # Continue processing the request
        response = self.get_response(request)
        return response
