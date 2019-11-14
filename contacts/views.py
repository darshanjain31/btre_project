from django.shortcuts import render,redirect,reverse
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def contact(request):
    if request.method=='POST':
       listing_id=request.POST['listing_id']
       listing = request.POST['listing']
       name = request.POST['name']
       email = request.POST['email']
       phone = request.POST['phone']
       message = request.POST['message']
       user_id = request.POST['user_id']
       realtor_email = request.POST['realtor_email']

       # check if user has made inquiry already

       if request.user.is_authenticated:
           #user_id=request.user.id
           has_contacted=Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
           if has_contacted:
               messages.error(request,'You have already made an inquiry for this listing')
               return redirect(reverse('listings:listing',args=(listing_id)))

       contact=Contact(listing=listing,listing_id=listing_id,name=name,email=email,phone=phone,message=message,user_id=user_id)
       contact.save()
       #send mail
       send_mail('Property listing inquiry',
                 'There has been inquiry for ' + listing +'. Sign in to admin panel for more info',
                  settings.EMAIL_HOST_USER,
                 [realtor_email,'jaindarshan3112@yahoo.com'],
                 fail_silently=False
                 )
       messages.success(request,'Your request has been submitted, a realtor will get back to you soon')
       return redirect(reverse('listings:listing',args=(listing_id)))
