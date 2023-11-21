from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('account:login')
    else:
        form = UserCreationForm()
    
    return render (request, 'account/register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login (request, user)
            return redirect('webapp:image_upload')
    else:
        form = AuthenticationForm()
    
    return render (request, 'account/login.html', {'form':form})


def logout_view(request):
    logout (request)
    return redirect ('account:login')
@login_required
def delete_view(request):
    return render (request, 'account/delete.html')
    

def yes(request):
    request.user.delete()
    messages.success(request,'YOUR ACCOUNT HAS BEN DELETED')
    return redirect ('account:login')  