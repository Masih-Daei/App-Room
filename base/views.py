from django.shortcuts import render,redirect
from .models import Room , Topic , Message,User
from django.db.models import Q
from .forms import RoomForm ,UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import newUserCreationForm


def registerPage(request):
    form = newUserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'error : we can`t create user')
    return render(request, 'base/login_register.html',{'form':form})


# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            
            login(request, user)
            return redirect('index')  
        else:
          
            messages.error(request, "User not found!")
    
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('index')
def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q )|
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    topics = Topic.objects.all()[0:3]
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains = q ))
    context = {'rooms':rooms , 'topics':topics , 'room_count':room_count,'room_message':room_message}
    return render(request,'base/index.html',context)

def room (request,pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room ,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room ,'messages':messages,'participants':participants}
    return render(request,'base/room.html',context)
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        room=form.save(commit=False)
        room.host = request.user
        room.save()
        return redirect('index')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room  = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you`re not allowed ')
    
    if request.method == "POST":
        room.delete()
        return redirect('index')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message  = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('you`re not allowed ')
    
    if request.method == "POST":
        message.delete()
        return redirect('index')
    return render(request,'base/delete.html',{'obj':message})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    context ={'user':user,'rooms':rooms,'room_message':room_message,'topics':topics }
    return render(request,'base/profile.html',context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    context ={'topics':topics}
    return render(request,'base/topics.html',context)

def activity_Page(request):
    room_message = Message.objects.all()
    context ={'room_message':room_message}
    return render(request,'base/activity.html',context)

def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    context ={'form':form}
    return render(request,'base/user_edit.html',context)