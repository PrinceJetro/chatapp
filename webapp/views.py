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
from .serializers import StudentSerializer
from .models  import *
from email.message import EmailMessage
import ssl
import smtplib

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

        # Assign the URL of the uploaded image
        global url 
        url = storage.url(filename)
    else:
        # If no image is uploaded, provide a default image URL
        # You can replace 'default_image_url' with the actual URL of your default image
        image_url = 'default_image_url'

    # Create the complaint object with the extracted data
    complaint = Complaint.objects.create(
        body=data["complaint"],
        categories=data["category"],
        img=image_url,  # Assign the URL of the image (either uploaded or default)
        image_link=image_url
    )

    # Serialize the complaint object
    serializer = ComplaintSerializer(complaint, many=False)

    # Return the serialized data in the response
    return Response(serializer.data)



@api_view(["POST"])
def createStudent(request):
    data = request.data
    email = data.get("email", None)
    
    if email is not None:
        # Check if the email already exists in the database
        existing_student = OnlineClass.objects.filter(email=email).first()
        if existing_student:
            return Response({"error": "Email already exists"}, status=400)

    # If email is not found or unique, proceed to create the student entry
    student = OnlineClass.objects.create(
        full_name=data["full_name"],
        phone_number=data["phone"],
        email=email,
        more=data["more"],
    )

    # Serialize the student object
    serializer = StudentSerializer(student, many=False)

    # Email content
    sender_email = 'adegbuyijephthah@gmail.com'
    password = "olyg kany wqzi gnwf"
    subject = "You have Successfully registered for the Web Development Class"
    body = f"""
Dear {data['full_name']},

Thank you for registering for the Web Development class with PrinceJetro Web Dev Training! We're excited to have you onboard.

Here are some details about the course:
- Course Schedule: Saturdays, starting from the 1st of June, from 1:00 PM to 4:00 PM via Zoom/Google Meet (3 hours per session)
- Target Audience: Beginners with at least 35% knowledge of HTML (not suitable for absolute beginners)
- Teaching Approach: Project-driven classes with a focus on practical application
- Interactive Learning: Engage in interactive sessions with hands-on projects
- Free Trial: The first class is free of charge
- Course Fee: Subsequent classes are paid, at a token of N2500 per class
- Duration: The course runs for 3 months
- Learning Resources: Access to shared resources and materials
- One-on-One Sessions: Personalized one-on-one sessions with instructors
- Additional Learning Materials: Links to YouTube videos for further learning
- Assignment Projects: Projects assigned after every class to reinforce learning

Please stay tuned for further communication regarding the course. If you have any questions or need assistance, feel free to reach out to us at adegbuyijephthah@gmail.com or call Jephthah Adegbuyi at 2348088981691.

We look forward to embarking on this learning journey with you!

Best regards,
PrinceJetro Web Dev Training
"""

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, email, f"Subject: {subject}\n\n{body}")

    return Response(serializer.data)



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














































# url = ''
# @api_view(["POST"])
# def createComplaint(request):
#     data = request.data

#     # Extract the uploaded image from the request data
#     image_file = request.FILES.get('image')

#     if image_file:
#         # If an image is uploaded, save it to Supabase storage
#         storage = SupabaseStorage()
#         post = 'anonymous/' + image_file.name
#         try:
#             filename = storage.save(post, image_file)
#             image_url = storage.url(filename)
#         except:
#             return HttpResponse("Failed to upload image to Supabase storage. Please try again.")

#         # Create the complaint object with the extracted data
#         global url 
#         url = storage.url(filename)
#         print(url)
#         complaint = Complaint.objects.create(
#             body=data["complaint"],
#             categories=data["category"],
#             img=url,  # Assign the URL of the uploaded image
#             image_link=url
#         )

#         # Serialize the complaint object
#         serializer = ComplaintSerializer(complaint, many=False)

#         # Return the serialized data in the response
#         return Response(serializer.data)

#     else:
#         return HttpResponse("No image uploaded")

