from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import django.utils.timezone

# Create your views here.
from .models import *
from .forms import createUserForm, createServerAllocation, changeServerAllocation

from . import server

from .config import config
import datetime

def home(request):
    print('here')
    serverIsLive = server.ping(config['serverIp'])
    print('after ping ')
    if not request.user.is_authenticated :
        context = {'serverIsLive' : serverIsLive, 'nextShutdown' : server.nextShutdown()}
        print('here unautheticated')
        return render(request, 'main/sites/dashboard.html', context)

    createAllocationForm = createServerAllocation(request.user)
    changeAllocationForm = changeServerAllocation()
    currentAllocations =  ServerAllocation.objects.filter(user=request.user, endTime__gte = server.now()).order_by("-startTime") #endtime >= now
    allocationHistory = ServerAllocation.objects.filter(user=request.user, endTime__lt = server.now()).order_by("-startTime")  #endTime < now
    django.utils.timezone.activate(config["TZ"])
    print('here pre context')
    context = {
        'serverIsLive' : serverIsLive,
        'nextShutdown' : server.nextShutdown(),
        "currentAllocations" : currentAllocations,
        "allocationHistory" : allocationHistory,
        'createAllocationForm' : createAllocationForm,
        'changeAllocationForm' : changeAllocationForm
    }
    print('post context')
    return render(request, 'main/sites/dashboard.html', context)

def nextShutdown(request):
    django.utils.timezone.activate(config["TZ"])
    context = {
        'nextShutdown' : server.nextShutdown(),
    }
    return render(request, 'main/sites/nextShutdown.html', context)

def timeTillNextShutdown(request):
    context = {
        'nextShutdown' : server.nextShutdown(),
    }
    return render(request, 'main/sites/timeTillNextShutdown.html', context)

@login_required(login_url='login')
def createAllocation(request):
    if request.method != "POST":
        return redirect("home")
    
    form = createServerAllocation(request.user, request.POST)
    if not form.is_valid():
        messages.error(request, "bad form")
        return HttpResponse("bad form")
    duration = int(form.cleaned_data.get('durationInHours'))
    ServerAllocation.objects.create(
        user = request.user,
        startTime = server.now(),
        endTime = server.now() + datetime.timedelta(hours=duration)
    )
    messages.success(request, "created Allocation") 
    return redirect("home")

@login_required(login_url='login')
def changeAllocation(request):
    if request.method != "POST":
        return redirect("home")
    form = changeServerAllocation(request.POST)
    if not form.is_valid():
        messages.error(request, "bad form")
        return HttpResponse("bad form")
    id = int(form.cleaned_data.get('id'))
    active = form.cleaned_data.get('active')
    try:
        allocation = ServerAllocation.objects.get(id=id)
    except ServerAllocation.DoesNotExist:
        messages.error(request, "not Found")
        return HttpResponse("not Found")
    
    if allocation.user != request.user:
        messages.error(request, "permission denied")
        return HttpResponse("permission denied")
    
    if allocation.endTime < server.now():
        messages.error(request, "permission denied")
        return HttpResponse("permission denied")
    
    allocation.active = active
    allocation.save()
    messages.success(request, "allocation changed")

    ## TODO Test

    return redirect("home")

@login_required(login_url='login')
def power_on_Page(request):
    if not request.user.is_superuser:
        messages.error(request, 'Permission denied')
        return redirect('home')
    
    try:
        result = server.controllServer(True)
        if result:
            messages.success(request, 'Server is starting.')
        else:
            messages.error(request, 'Something went wrong.')
    except server.alreadyOn:
        messages.info(request, 'Server is already on.')
    except server.alreadyStarting:
        messages.info(request, 'Server is already starting.')

    return redirect('home')

@login_required(login_url='login')
def power_off_Page(request):
    if not request.user.is_superuser:
        messages.error(request, 'Permission denied')
        return redirect('home')
    try:
        result = server.controllServer(False)
        if result:
            messages.success(request, 'Server is stopping')
        else:
            messages.error(request, 'Something went wrong')
    except server.alreadyOff:
        messages.info(request, 'Server is already stopped.')

    return redirect('home')
    

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            username = user.get_username() 
            messages.success(request, 'Successfully logged in as ' + username )
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'main/sites/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = createUserForm()
    if request.method == 'POST' :
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
   
    context = {'form' : form}
    return render(request, 'main/sites/register.html', context)