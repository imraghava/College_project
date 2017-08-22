from django.shortcuts import render,render_to_response,redirect
from django.conf import settings
from UnistashFinal.settings import SENDER,PASS
import smtplib
from django import forms
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views import generic
from .forms import UserForm ,ContactForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm ,UserFormlog, ProfileForm
from django.template import RequestContext
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User #as auth_user
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from .models import students
from django.views.decorators.cache import cache_control
from .models import Profile

@cache_control(no_cache=True, must_revalidate=True)    
def index(request,string=None):
  msgs=''
  a=string 
  template = a+'.html'
  student=request.user
  abc=Profile
  if student.username:
      k=student.id
      abc=Profile.objects.get(user_id=k)
   
  # here student is used for putting name on every page
  if a=='index' or a=='notes' or a=='papers' or a=='practical-files': 
   if request.method == 'GET':
      user_form = UserForm(request.GET)
      profile_form=ProfileForm
      return render(request, template, {'student':student,'abc':abc,
           'user_form': user_form  , 'profile_form':profile_form,'msgs' : msgs       })

      
   if request.method == 'POST':
      user_form = UserForm(request.POST)
      profile_form=ProfileForm(request.POST)
      if  user_form.is_valid()  :
           
           user1= user_form.save(commit=False)
           #prof= profile_form.save()
           username = user_form.cleaned_data['username']
           fname = user_form.cleaned_data['first_name']
           password = user_form.cleaned_data['password']
           email = user_form.cleaned_data['email']
           user1._photo=request.FILES['photo']#,False]            
         
           user1.set_password(password)
           
           user1.save()
           msg="Hello , \n Welcome to Unistash . Thanks for joining us. We will keep you updated!!"

           smtp= smtplib.SMTP('smtp.gmail.com')
           smtp.ehlo()
           smtp.starttls()
           smtp.ehlo()
           smtp.login(SENDER,PASS)
           smtp.sendmail(SENDER,email,msg)
           smtp.quit()
           #profile=profile_form.save(commit=False)
           #profile.user_id=user1.id+1
           #profile.college=profile_form.cleaned_data['college']
           #profile.save()
           
          
           #profile_form.save()
            #return redirect('settings:profile')
           msgs='Thanks for joining us..'
           user_form = UserForm(request.GET)
      
      return render(request, template, {
           'user_form': user_form  , 'profile_form':profile_form,'msgs' : msgs ,'abc':abc ,'student':student     })

   else:
     
           msgs='not sent'
           return render(request,template , {  'user_form': user_form  , 'profile_form':profile_form,
                                               'msgs' : msgs })
	

  elif a=='Aboutus':

   if request.method == 'GET':
      user_form = ContactForm(request.GET)
      
      return render(request, template, {
           'user_form': user_form  , 'msgs' : msgs       })

      
   if request.method == 'POST':
      user_form = ContactForm(request.POST)
       
      if  user_form.is_valid()  :
           
           user1= user_form.save(commit=False)
           #prof= profile_form.save()
           email = user_form.cleaned_data['email']
           name = user_form.cleaned_data['name']
           message = user_form.cleaned_data['message']
           
           msg=email +' '+ name+' ' + message
           smtp= smtplib.SMTP('smtp.gmail.com')
           smtp.ehlo()
           smtp.starttls()
           smtp.ehlo()
           smtp.login(SENDER,PASS)
           smtp.sendmail(SENDER,SENDER,msg)
           smtp.quit()
           #profile=profile_form.save(commit=False)
           #profile.user_id=user1.id+1
           #profile.college=profile_form.cleaned_data['college']
           #profile.save()
         
          
           #profile_form.save()
            #return redirect('settings:profile')
           msgs='Thanks for contacting us..'
           user_form = ContactForm(request.GET)
      
      return render(request, 'Aboutus.html', {
           'user_form': user_form  , 'msgs' : msgs       })

   else:
           msgs='not sent'
           return render(request,template , {  'user_form': user_form  , 'profile_form':profile_form,
                                               'msgs' : msgs })
	
# this is the last one for all the pages
  elif a=='login':
   ab="Not Registered user..."
   user_form = UserForm(request.GET)
   student =request.user
   
   if student.username:
      k=student.id
      abc=Profile.objects.get(user_id=k)
      return render(request,'contribute.html',{'student':student,'abc':abc})#,{'user_form':user_form} )
        
   else: 
    if request.method == 'GET':
         user_form = UserFormlog(request.GET)
         return render(request, 'login.html', {
        'user_form': user_form    #user_form
    })

    if request.method == 'POST':
        user_form1 = UserFormlog(request.POST)
        user_form = UserForm(request.GET)
       
        if user_form1.is_valid() :
           ab="post chala"       
     
           #prof= profile_form.save()
           username = user_form1.cleaned_data['username']
           password = user_form1.cleaned_data['password']
           #profile=profile_form.save(commit=False)
           #profile.user_id=user1.id+1
           #profile.college=profile_form.cleaned_data['college']
           #profile.save()
         
           user1 = authenticate(username=username ,password=password)
           print user1
           if user1 :
             print "db me hai"
             
             ab="db me hai"
           else:
             print "db me nai hai"
           if user1 :
             auth.login(request, user1)
                #return redirect('index.html')
             return render(request,'contribute.html',{ 'student': user1 })#,{'user_form':user_form} )
              
           else:
                #return redirect('nope.html')
                return render(request,'nope.html')
        
           #profile_form.save()
            #return redirect('settings:profile')
        
    return render(request, 'login.html', {
        'user_form': user_form1 ,'ab':ab
    })

  else:

     return render(request,template,{  'student':student} )

@cache_control(no_cache=True, must_revalidate=True)    
def logout(request):
    user_form1=request.user
    user_form= UserFormlog
    ab="Logged out"
    #print user_form1
    user_form1=None
    auth.logout(request)
    request.session.flush()
    for key in request.session.keys():
      del request.session[key]
   # del request.session[user_form1]
    #user_form1= users.objects.filter(user__username=request.user)
    #user_form1.username=''
    #return redirect(userlogin)
    return render(request, 'login.html', {
        'user_form': user_form ,'ab':ab
    })
def index1(request,string=None):
  msgs=''
  a=string 
  template = a+'.html'
  user_form = UserFormlog
        

 # if a=='index' or a=='notes' or a=='papers' or a=='practical-files': 
 #  if request.method == 'GET':
 #     user_form = UserForm(request.GET)
      
  return render(request, template, {'user_form': user_form  , 'msgs' : msgs       })

      
 
	
def file1(request,string=None):
        #try:
        # return FileResponse(open('C:\Users\HCL\Unistash\unistash\Unistash\media\hass.pdf', 'rb'), content_type='application/pdf')
        #except FileNotFoundError:
         #raise Http404()
         q=string
         with open('D:/College_Project/UnistashFinal/media/'+q+'.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'filename=hass.pdf'
            return response



def company(request ,company=None):
   number=students.objects.filter(company=company)
   context= {
       'numberofstudents' : number
     }
   
   return render(request, 'CompanyInterview.html',context  )
