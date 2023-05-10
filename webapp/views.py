from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import login, authenticate, logout #add thi
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Q
from email.message import EmailMessage
from .models  import *
from django.test import Client
import json
from .forms import  *
from django.core import serializers
from django.http import JsonResponse
from webapp.storage import SupabaseStorage
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == 'POST':
        username = request.POST["username"]
        password1 = request.POST["psw1"]
        password2 = request.POST["psw2"]
        email = request.POST["email"]

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "UserName Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username = username,email=email, password= password1 )
                user.save()
                auth.login(request, user)
        else:
            messages.info(request, "Password not matching")
            return redirect('register')
        return redirect(reverse("avatar", kwargs={'pk': user.id}))
    
    else:
        return  render(request, 'register.html')


def Avatar(request,pk):
    form = AvatarForm(request.POST, request.FILES)
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            print("yass")
            image = form.cleaned_data['avatar']
            storage = SupabaseStorage()
            post = 'chatapp_profile_pic/' + image.name
            try:
                filename = storage.save(post, image)
            except:
                return HttpResponse("Please upload another image, this image already exists")

            global url 
            url = storage.url(filename)
            user = User.objects.get(id=pk)
            user.image_link = url
            user.save()
            print(url)
            return redirect("login")
    return render(request, 'profilepic.html', {"form" : form})


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(username)
        user = auth.authenticate(username=username, password=password)
        

        if user is not None:
            auth.login(request, user)
            return redirect(reverse('home'))
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, "login.html")
    

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")

@login_required(login_url='login')
def home(request):
    users = User.objects.all()
    q = request.GET.get('q') if request.GET.get("q") != None else ''
    room = Room.objects.filter(
        Q(host__username__icontains=q) |
        Q(name__icontains=q)

    )



    context = {
        "rooms" :  room,
    }
    return render(request, "index.html", context)


def userProfile(request,pk):
    user =  User.objects.get(id=pk)
    rooms = user.room_set.all()
    context = {
        'user': user,
        "rooms"  :rooms
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def chatroom(request,pk):
    
    room = Room.objects.get(id=pk)
    print(room.host.id)
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect('chatroom',pk=room.id)  
    
    room_messages = room.message_set.all().order_by("-created")
    for i in room_messages:
        print(i.created)
    context = {"rooms": room, 'room_messages': room_messages, 'participants': participants}
    print(room)
    return render(request, 'chat.html', context)



# def get_latest_items(request,pk):
#     room =  Room.objects.get(id=pk)
#     items = room.message_set.all().order_by("-created")
#     data = serializers.serialize('json', items)
#     return JsonResponse(data, safe=False)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid:
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("home")    
    context =  {
        'form':form
    }
    return render(request, "room_form.html", context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render( request,'delete.html', {'obj': room})




@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not  allowed here")
    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render( request,'delete.html', {'obj': message})













































'''
def chatroom(request, username):
    room = get_object_or_404(ChatRoom, name=username)
    message = room.messages.all()
    for i in message:
        i.aux = str(i.sender)
        #print(i.aux)
        #print(type(i.aux))
        #print(type(room.name))
        #print(room.name == i.aux)
    context = {
        "room": room,
        "message" : message,
    }
    print(room.name == request.user.username )
    return  render(request, "chat.html", context)




    ChatMessage.objects.create(sender= request.user, content=content, aux="aux", receiver=request.user,room=room)

    return redirect(reverse('chatroom', kwargs={'username': room.name}))'''