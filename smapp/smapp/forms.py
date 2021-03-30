from django import forms

class SEM(forms.Form):
    sender = forms.EmailField()
    receiver = forms.EmailField()
    subject = forms.CharField()
    email_content = forms.CharField(widget=forms.Textarea)
    #attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class OTP(forms.Form):
    otp_token = forms.CharField(max_length=6)
    msg_id = forms.CharField(widget=forms.HiddenInput())
