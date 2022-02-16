from email import message
from hashlib import new
import imp
from random import randint
from signal import alarm
from unittest import result
from django.shortcuts import redirect, render
# from django.http import HttpResponse
from.models import Register
from django.contrib.auth.models import User,auth
from django.contrib import messages

from .SMS import SMS
from .Mail import Mail
# Create your views here.

# page

def home_page(request):
    #Query DData From Model
    data = Register.objects.all()
    return render(request,'index.html',{'regs' : data} )

def page1(request):
    return render(request,'page1.html')

def register_page(request):
    return render(request,'register_page.html')

def otp_page(request):
    return render(request,'otp_page.html')

def result_page(request):
    print(request.POST)
    data =  {
                'first_name':   request.POST['first_name'],
                'last_name':    request.POST['last_name'],
                'username':     request.POST['username'],
                'password':     request.POST['password'],                
                'email':        request.POST['email'],

                'birthday':     request.POST['birthday'],
                'tel':          request.POST['tel'],
                'address':      request.POST['address'],
                'city':         request.POST['city'],
                'country':      request.POST['country'],
                'zip_code':     request.POST['zip_code'],

                # 'file_id':      request.FILES['file_id'],
                # 'file_face':    request.FILES['file_face'],


                'otp_sms':      request.POST['otp_sms1'],
                'otp_email':    request.POST['otp_email1']
            }

    print(request.POST['first_name'])
    if request.POST['otp_sms1'] == request.POST['otp_sms2']:
        if request.POST['otp_email1'] == request.POST['otp_email2']:

            user = User.objects.create_user(
            username    = request.POST['username'],
            password    = request.POST['password'],
            email       = request.POST['email'],
            first_name  = request.POST['first_name'],
            last_name   = request.POST['last_name']
            )
            user.save()

            register = Register.objects.create(
                birthday    = request.POST['birthday'],
                tel         = request.POST['tel'],
                address     = request.POST['address'],
                city        = request.POST['city'],
                country     = request.POST['country'],
                zip_code    = request.POST['zip_code'],
                # file_id     = request.FILES['file_id'],
                # file_face   = request.FILES['file_face'],
                user        = user
            
            )


            return render(request,'result.html')
    return render(request,'otp_page.html',data)

def login_page(request):
    return render(request,'login_page.html')

def profile_page(request):
    return render(request,'profile_page.html')
# method


    
def add_user(request):
    username    = request.POST['username']
    email       = request.POST['email']
    password1   = request.POST['password1']
    password2   = request.POST['password2']
    is_password_checked,result =  password_check(password1)
    if password1 != password2:
        msg = "Password does not match"
        print(msg)
        messages.warning(request,msg)

    # elif not is_password_checked:
    #     msg = "This password is too simple."
    #     print(msg)
    #     messages.warning(request,msg)

    elif User.objects.filter(username = username).exists():
        msg = "This username is already taken."
        print(msg)
        messages.warning(request,msg)


    elif User.objects.filter(email = email).exists(): 
        msg = "This email is already taken."
        print(msg)
        messages.warning(request,msg)
    else:
                
        otp_sms = str(randint(0,9999)).zfill(6)
        otp_email = str(randint(0,9999)).zfill(6)

        otp = SMS()        
        otp.send_otp("+66929746129",otp_sms)
            
        mail = Mail()
        mail.send_otp(email,otp_email)

        data =  {
                    'first_name':   request.POST['first_name'],
                    'last_name':    request.POST['last_name'],
                    'username':     request.POST['username'],
                    'password':     request.POST['password1'],
                    'email':        request.POST['email'],
                    'birthday':     request.POST['birthday'],
                    'tel':          request.POST['tel'],
                    'address':      request.POST['address'],
                    'city':         request.POST['city'],
                    'country':      request.POST['country'],
                    'zip_code':     request.POST['zip_code'],

                    # 'file_id':      request.FILES['file_id'],
                    # 'file_face':        request.FILES['file_face'],

                    'otp_sms':      otp_sms,
                    'otp_email':    otp_email
                }
        return render(request,'otp_page.html',data)
    return redirect('/register_page')

def add_form(request):
    first_name  = request.POST['first_name']
    last_name   = request.POST['last_name']
    username    = request.POST['username']
    email       = request.POST['email']
    password1   = request.POST['password1']
    password2   = request.POST['password2']

    if password1 != password2:
        print("password not same")
        messages.warning(request,"password not same")
        
    elif User.objects.filter(username = username).exists():
        print("Same Username")
        messages.warning(request,"Same Username")

    elif User.objects.filter(email = email).exists(): 
        print("Same Email")

    else:
        user = User.objects.create_user(
            username    =username,
            password    = password1,
            email       = email,
            first_name  = first_name,
            last_name   = last_name
            )
        user.save()
        return render(request,'result.html',
        {
            'name': first_name
        })
    return redirect('/page1')

def login(request):
    username=request.POST['username']
    password=request.POST['password']

    #check username ,password
    user=auth.authenticate(username=username,password=password)

    if user is not None :
       auth.login(request,user)
       return redirect('/profile_page')
    else :
        messages.info(request,'Wrong username or password. Press try again.')
        return redirect('/login_page')
    
def logout(request):
    auth.logout(request)
    return redirect('/')
# function
def password_check(passwd):
      
    SpecialSym =['$', '@', '#', '%']
    val = True
    result = ""
    if len(passwd) < 6:
        result = 'length should be at least 6'

        val = False
          
    elif len(passwd) > 20:
        result = 'length should be not be greater than 20'
        val = False
          
    elif not any(char.isdigit() for char in passwd):
        result = 'Password should have at least one numeral'
        val = False
          
    elif not any(char.isupper() for char in passwd):
        result = 'Password should have at least one uppercase letter'
        val = False
          
    elif not any(char.islower() for char in passwd):
        result = 'Password should have at least one lowercase letter'
        val = False
          
    elif not any(char in SpecialSym for char in passwd):
        result = 'Password should have at least one of the symbols $@#'
        val = False

    if not result=='':
        print(result)
    return val,result

