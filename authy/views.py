
from django.shortcuts import render, redirect
from .models import NewUser, Address
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .utils import generate_token
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginpage(request):
    if not request.user.is_authenticated:
        return render(request,'authy/login.html')
    else:
        return redirect('/')

def registerpage(request):
    if not request.user.is_authenticated:
        return render(request,'authy/register.html')
    else:
        return redirect('/')

def logging(request):
    if request.method=='POST':
        mail = request.POST.get('email', '')
        user_password = request.POST.get('password', '')
        user = authenticate(username=mail, password=user_password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')

def registration(request):
    if request.method=='POST':
        email = request.POST.get('email')
        userCheck = NewUser.objects.filter(email=email)
        phone = request.POST.get('phone')
        userPhone = NewUser.objects.filter(phone=phone)
        if userCheck or userPhone:
            return redirect('/register/')
        else:
            name = request.POST.get('name')
            dob = request.POST.get('dob')
            password = request.POST.get('password')
            user_obj = NewUser.objects.create_user(first_name=name, phone=phone, password=password,
                                                   email=email, user_name=email, dob=dob)
            user_obj.save()

            current_site = get_current_site(request)
            email_sub = "Activate your account"

            message = render_to_string('authy/activate.html',
                                       {
                                           'user': user_obj,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
                                           'token': generate_token.make_token(user_obj),
                                       })
            email = EmailMultiAlternatives(
                subject=email_sub,
                body='',
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )
            email.attach_alternative(message,"text/html")
            try:
                email.send()
                return redirect('/login')
            except:

                return redirect('/register')



def user_logout(request):
    logout(request)
    return redirect('/login')


def activateView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = NewUser.objects.get(pk=uid)

    except:
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('/')
    else:
        return redirect('/register')



@login_required
def addAddress(request):
    if request.method=='POST':
        address=request.POST.get('address')
        type=request.POST.get('type')
        state=request.POST.get('state')
        zip=request.POST.get('zip')
        add=Address(
            user=request.user,
            address=address,
            type=type,
            pin=zip,
            state=state
        )
        add.save()
        return redirect('/shop/checkout')