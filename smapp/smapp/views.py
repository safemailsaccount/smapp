from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.core.mail import send_mail
from cryptography.fernet import Fernet
import pyotp
import time
from .models import Message
from .forms import SEM
from .forms import OTP

def home(request):
    return render(request, 'sm/home.html')

def send(request):
        if request.method == "POST":
            filled_form = SEM(request.POST)
            if filled_form.is_valid():
                note = 'Thanks for using Safemails.Net! Your Encrypted Email to [%s] is on its way!' %(filled_form.cleaned_data['receiver'],)
                new_form = SEM()
                sender = filled_form.cleaned_data['sender']
                print (sender)
                receiver = filled_form.cleaned_data['receiver']
                subject = filled_form.cleaned_data['subject']
                email_content = filled_form.cleaned_data['email_content']
                unique_id = get_random_string(length=32)
                ins = Message(msg_id=unique_id, email_content=email_content, receiver=receiver, sender=sender, subject=subject)
                ins.save()
                print("The data has been written to DB")
                #subject = 'Encrypted Email'
                body = '%s sent you an encrypted message. Please click the link to decrypt it.\n\n <a href=https://www.safemails.net/smapp/auth/%s>Decrypt Message</a> \n\nPowered by Safemails.Net. The Painless Dencryption.' %(sender, unique_id)
                send_mail(subject, body, sender, [receiver,])
                print("Email was sent!")
                return render(request, 'sm/send.html', {'sem':new_form, 'note':note})
        else:   
            form = SEM()
            return render(request, 'sm/send.html', {'sem':form})

def auth_post(request):
        if request.method == "POST":
            new_form = OTP()
            #base32secret = pyotp.random_base32()
            base32secret = 'HDUVCGVA2IBBLNNG'
            totp = pyotp.TOTP(base32secret)
            auth_form = OTP(request.POST)
            if auth_form.is_valid():
                    base32secret = 'HDUVCGVA2IBBLNNG'
                    #base32secret = pyotp.random_base32()
                    totp = pyotp.TOTP(base32secret)
                    returned_token = auth_form.cleaned_data['otp_token']
                    here_token = totp.now()
                    if returned_token == here_token:
                        print('You are authenticated!')
                        msg_str=auth_form.cleaned_data['msg_id']
                        select_qulified_content = Message.objects.get(msg_id=msg_str)
                        email_content=select_qulified_content.email_content
                        sender=select_qulified_content.sender
                        subject=select_qulified_content.subject
                        print(sender)
                        #key = Fernet.generate_key()
                        #f = Fernet(key)
                        #encrypted_email_content = f.encrypt(email_content)
                        #print(email_content)
                        #print(encrypted_email_content)
                        return render(request, 'sm/decr.html',{'sender':sender, 'subject':subject,'email_content':email_content})
                    else:
                        print('Wrong PIN. To read the email you must provide PIN your see on your phone. Try again!')
                        return render(request, 'sm/auth.html', {'otp':new_form}) 
            else:
                print('secondlevel.Try again!')
                return render(request, 'sm/auth.html', {'otp':new_form})                 
        else:
            print('firstlevel.Try again!')
            new_form = OTP()
            return render(request, 'sm/auth.html', {'otp':new_form})              
def auth_get(request, msg_id):       
        if request.method == "GET":
            form = OTP()
            form = OTP(initial={'msg_id': msg_id})
            key = Fernet.generate_key()
            f = Fernet(key)
            #msg_str=auth_form.cleaned_data['msg_id']
            select_qulified_content = Message.objects.get(msg_id=msg_id)
            email_content=select_qulified_content.email_content
            bytes_email_content=email_content.encode()
            encrypted_email_content = f.encrypt(bytes_email_content)
            str_email_content=encrypted_email_content.decode()
            print(str_email_content)
            #base32secret = pyotp.random_base32()
            base32secret = 'HDUVCGVA2IBBLNNG'
            #base32secret = pyotp.random_base32()
            #totp_uri = pyotp.totp.TOTP(base32secret).provisioning_uri(
            #"kosta@google.com",
            #issuer_name="SAFEMAIL_NET")
            #print(totp_uri)
            qr_code = 'https://quickchart.io/qr?text=otpauth://totp/SAFEMAIL_NET:kosta@safemails.net?secret=HDUVCGVA2IBBLNNG&issuer=SAFEMAIL_NET'
            totp = pyotp.TOTP(base32secret)
        return render(request, 'sm/auth.html', {'otp':form, 'qr_code':qr_code, 'str_email_content':str_email_content})
