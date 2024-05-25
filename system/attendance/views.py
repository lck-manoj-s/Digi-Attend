from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from attendance.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,logout
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def ShowLoginPage(request):
    return render (request, "login.html")

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return HttpResponseRedirect(reverse('admin_home'))
            elif user.user_type == '2':
                return HttpResponseRedirect(reverse('staff_home'))
            else:
                return HttpResponseRedirect(reverse('student_home'))
        else:
            messages.error(request,"Invalid Login request")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User:" + request.user.email+" user types as "+request.user.user_type)
    else:
        return HttpResponse("<h2> Please Login First </h2>")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
