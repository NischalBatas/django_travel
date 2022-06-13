from django.shortcuts import render,redirect
from .forms import UserAdminCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
# Create your views here.
from django.core.mail import send_mail
from .models import *
from .forms import *

def logins(request):
    if request.method=="POST":
        email=request.POST['email']
        passwords=request.POST['password']
        user=authenticate(request,username=email,password=passwords)
        if user is not None:
            login(request,user)
            return redirect('index')

    return render(request,'auth/logins.html')

def logouts(request):
    logout(request)
    return redirect('logins')

def signup(request):
    if request.method=="POST":
        form=UserAdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("successful")
            return redirect('index')
        else:
            print("Unsuccessful")
    else:
        form=UserAdminCreationForm()
    return render(request,'auth/signup.html',{"form":form})

def list(request):
    list=CustomUser.objects.all()
    context={
        "list":list
    }
    return render(request,'auth/list.html',context)

def contact(request):
    if request.method == 'POST':
        subjects = request.POST['subjects']
        messages = request.POST['messagess']

        message_from = request.POST['message_from']
        message_to=request.POST['message_to']

        send_mail(
        subjects,
        messages,
        message_from,
        [message_to],
        fail_silently=False,
        )
        return render(request, 'auth/contact.html', {'messages': messages,'message_from':message_from})
    else:
        return render(request, 'auth/contact.html')

def adduser(request):
    if request.method=="POST":
        form=UserAdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Successful")
            return redirect('logins')
    else:
        form=UserAdminCreationForm()
    return render(request,'auth/CRUD/adduser.html',{'form':form})

def updateuser(request,user_id):
    user=CustomUser.objects.get(pk=user_id)
    form=UserAdminCreationForm(request.POST or None, instance=user)
    if form.is_valid():
            form.save()
            return redirect('list')
  
    context={
            "form":form
        }
    return render(request,'auth/CRUD/updateuser.html',context)

def deleteuser(request,user_id):
    user=CustomUser.objects.get(pk=user_id)
    user.delete()
    return redirect("list")