from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .forms import RegistrationForm
from .models import CustomUser
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email is confirmed
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your crowdfunding account.'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(mail_subject, message, 'admin@crowdfunding.com', [user.email])

            return render(request, 'accounts/confirm_email.html')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')
    
    

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid login credentials or account not activated.')
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


