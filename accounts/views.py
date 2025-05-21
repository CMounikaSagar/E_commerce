from django.shortcuts import render,redirect,HttpResponse
from .forms import *
from store.views import *
from .models import Account
from carts.models import *
from carts.views import _cart_id
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('form is valid')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_no = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password,
            )
            user.phone_number = phone_no
            user.save()
            
            #Send User activation link to email
            
            current_site = get_current_site(request)
            mail_subject = 'Please activate your email'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uidb64':urlsafe_base64_encode(force_bytes(user.pk)), #encoding the userID
                'token':default_token_generator.make_token(user),
            })
            activation_url = f"http://{current_site.domain}{message}"
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # messages.success(request, 'Registration Successfull Please activate your account ')
            return redirect('/accounts/login/?command=verification&email='+email) 
        else:
            print(form.errors)
        
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request,'accounts/register.html',context)

def user_login(request):
    print("userloginview")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email = email , password = password)
        if user is not None:
            cart_id = _cart_id(request)

            try:
                cart,created = Cart.objects.get_or_create(cart_id = _cart_id(request)) #get the cart using the cart id using the session id
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    
                    cart_item = CartItem.objects.filter(cart=cart)
                    # assigning the user to cart item
                    for item in cart_item:
                        item.user = user
                        item.save()
            except Exception as e:
                pass
            login(request,user)
            messages.success(request,"Successfully login")
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid login credintials')
            print(user)
        return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request,'You are logged out')
    return redirect('login')

def activate_account(request,uidb64,token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations your account is activated')
        return redirect('login')
    else:
        messages.error(request,'Email activation link')
        return redirect(request)
    
@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

def forgot_pwd(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Account.objects.filter(email__exact=email).first()
        if user:
            
            # Reset your password
            current_site = get_current_site(request)
            mail_subject = 'Please activate your email'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uidb64':urlsafe_base64_encode(force_bytes(user.pk)), #encoding the userID
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            messages.success(request,'Password has been sent to email')
            return redirect('login')
        else:
            messages.error(request,'Account Does not exists')
            return redirect('forgot_pwd')
    return render(request,'accounts/forgot_pwd.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has expired')
        return redirect('login')
    
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password) #just saving password is not enough you have to use setpassword or else it shows error
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request,'Password reset successfully')
            return redirect('resetpassword')
    else:
        return render(request,'accounts/reset_password.html')
    

def editprofile(request):
    return request(request,'accounts/edit_profile.html')