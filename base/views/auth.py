# Django Modules
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

# Custom Modules Work as a tool
import random

# DataBase module import session
from base.models import OTPVerification

# Email Configuration modules
from django.core.mail import send_mail
from django.utils import timezone


from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def generate_otp():
    # Generate a 6-digit OTP (you can adjust the length as needed)
    return ''.join(random.choices('0123456789', k=6))

def enter_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return redirect('login')
        else:
            otp_value = generate_otp()
            send_mail(
                'Congratulations!',                         # subject
                'You are lucky to receive this mail.',      # body
                'sitejec@gmail.com',                        # sender Email
                [email],                                    # receiver mail
                html_message=f"<h1>Your otp is :</h1> <p>{otp_value}</p>",
                fail_silently=False,
            )
            otp_verification = OTPVerification(email=email,otp_key=otp_value)
            otp_verification, created = OTPVerification.objects.get_or_create(
                email=email,
                defaults={'otp_key': otp_value}
            )
            # If the email already existed, update the OTP value
            if not created:
                otp_verification.otp_key = otp_value
                otp_verification.updated_time = timezone.now()
                otp_verification.save()
            obj = OTPVerification.objects.get(email=email)
            print("otp sent...", otp_value, "last updated value is : ", obj.otp_key)
            return redirect('signup', mail=email)
    return render(request,"auth/otp_verification.html")


def signup(request, mail):
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Check if the username is already taken
            obj = OTPVerification.objects.get(email=mail)
            # check if the otp is match or not
            if otp == obj.otp_key:
                time_difference = timezone.now() - obj.updated_time
                if time_difference.total_seconds() <= 120:  # 120 seconds = 2 minutes
                    if User.objects.filter(username=username).exists():
                        return render(request, "auth/signup.html", {"mail":mail, "msg":"User name already exist. try any different name"})
                    else:
                        # Create the user
                        user = User.objects.create_user(username=username, email=mail, password=password)
                        login(request, user)
                        return redirect('home')  # Redirect to your home page
                else:
                    # The OTP was not updated within the last 2 minutes, handle accordingly
                    return render(request, "auth/signup.html", {"mail":mail, "msg":"The Otp is expired. So again enter the password create new one. <a href='enter_otp'>click here</a> to redirect"})
            else:
                return render(request, "auth/signup.html", {"mail":mail, "msg":"The Otp do not match, Try again"})
        else:
            return render(request, "auth/signup.html", {"mail":mail, "msg":"Passwords do not match"})
    
    return render(request, 'auth/signup.html',{"mail":mail})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your home page
        else:
            return HttpResponse("Invalid login credentials")
    
    return render(request, 'auth/login.html')


def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Check if the current password matches the user's password
        if user.check_password(current_password):
            # Check if the new password matches the confirm password
            if new_password == confirm_password:
                # Set the new password
                user.set_password(new_password)
                user.save()

                # Update the user's session to prevent logout
                update_session_auth_hash(request, user)

                # Redirect to a success page or return a success message
                return HttpResponse("Password changed successfully!")
            else:
                # Return an error message for mismatched passwords
                return HttpResponse("New password and confirm password do not match!")
        else:
            # Return an error message for incorrect current password
            return HttpResponse("Incorrect current password!")

    # Handle GET requests if needed
    return render(request, 'auth/change_password.html')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"
            
            # Send reset link to user's email address
            send_mail(
                'Password Reset Link',                              # Subject
                f'Click the link below to reset your password:\n{reset_link}',  # Body
                'your_email@example.com',                           # Sender's Email
                [email],                                            # Receiver's Email
                fail_silently=False,                                # If True, errors will be silently ignored
            )
            
            messages.success(request, "Password reset link has been sent to your email.")
            # return redirect('login')
        else:
            messages.error(request, "Email not found.")
    return render(request, 'auth/forgot_password.html')

def logout_view(request):
    logout(request)
    return redirect('login') 


def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
  
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if new_password1 == new_password2:
                # Set the new password
                user.set_password(new_password1)
                user.save()

                # Update the user's session to prevent logout
                update_session_auth_hash(request, user)
                user = authenticate(request, username=user.username, password=new_password1)
                print(user)

                # Redirect to the login page
                return redirect('login')
            else:
                messages.error(request, "New passwords do not match.")
                return render(request, 'auth/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})

        return render(request, 'auth/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
    else:
        # Invalid user or token, redirect to a page showing an error message
        messages.error(request, 'Invalid password reset link. Please try again.')
        return redirect('forgot_password')  # Replace 'forgot_password' with your forgot password URL name