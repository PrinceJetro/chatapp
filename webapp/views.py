from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
# from django.contrib import messages
# from django.contrib.auth.models import auth
# from django.contrib.auth import login, authenticate, logout #add thi
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404, redirect, render
# from django.urls import reverse
# from django.db.models import Q
# from email.message import EmailMessage
# from django.test import Client
# import json
# from .forms import  *
# from django.core import serializers
# from django.http import JsonResponse
from webapp.storage import SupabaseStorage
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ComplaintSerializer
from .models  import *
# Create your views here.


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {
            "endpoint": "/all"
        }
    ]
    return Response(routes)

@api_view(["GET"])
def getAll(request):
    note = Complaint.objects.all()
    serializer = ComplaintSerializer(note, many=True)
    json_data = serializer.data  # Convert serializer data to JSON format
    return JsonResponse(json_data, safe=False)  # Return JSON response




url = ''
@api_view(["POST"])
def createComplaint(request):
    data = request.data

    # Extract the uploaded image from the request data
    image_file = request.FILES.get('image')

    if image_file:
        # If an image is uploaded, save it to Supabase storage
        storage = SupabaseStorage()
        post = 'anonymous/' + image_file.name
        try:
            filename = storage.save(post, image_file)
            image_url = storage.url(filename)
        except:
            return HttpResponse("Failed to upload image to Supabase storage. Please try again.")

        # Create the complaint object with the extracted data
        global url 
        url = storage.url(filename)
        print(url)
        complaint = Complaint.objects.create(
            body=data["complaint"],
            categories=data["category"],
            img=url,  # Assign the URL of the uploaded image
            image_link=url
        )

        # Serialize the complaint object
        serializer = ComplaintSerializer(complaint, many=False)

        # Return the serialized data in the response
        return Response(serializer.data)

    else:
        return HttpResponse("No image uploaded")



#https://fmlguqqzwmsqgobmvzll.supabase.co/storage/v1/object/public/Jetro/anonymous/z166394.jpg
#/https%3A/fmlguqqzwmsqgobmvzll.supabase.co/storage/v1/object/public/Jetro/anonymous/z166394.jpg%3F
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