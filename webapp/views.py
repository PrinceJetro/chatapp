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
            return print("Failed to upload image to Supabase storage. Please try again.")

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

    # Email details
    sender_email = 'princejetro123@gmail.com'
    password = "iatu bier ypec yeqq"
    receiver_email = 'davidblessing603@gmail.com'
    subject = "Someone made a complaint"

    # Create the HTML body content
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <p>Dear Sir,</p>
        <p>Category: {data["category"]}</p>
        <p>Body: {data["complaint"]}</p>
        <p><img src="{image_url}" alt="Attached Image"></p>
    </body>
    </html>
    """

    # Create an EmailMessage object and set it up for HTML
    em = EmailMessage()
    em["From"] = sender_email
    em["To"] = receiver_email
    em["Subject"] = subject

    # Set the email content as HTML
    em.add_alternative(html_body, subtype="html")

    # Send the email via Gmail's SMTP server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(em)

    print(f"Email sent successfully to {receiver_email}!")

    # Return the serialized data in the response
    return Response(serializer.data)



# @api_view(["POST"])
# def createStudent(request):
#     data = request.data
#     email = data.get("email", None)
    
#     if email is not None:
#         # Check if the email already exists in the database
#         existing_student = OnlineClass.objects.filter(email=email).first()
#         if existing_student:
#             return Response({"error": "Email already exists"}, status=400)

#     # If email is not found or unique, proceed to create the student entry
#     student = OnlineClass.objects.create(
#         full_name=data["full_name"],
#         phone_number=data["phone"],
#         email=email,
#         more=data["more"],
#     )

#     # Serialize the student object
#     serializer = StudentSerializer(student, many=False)

#     # Email content
#     sender_email = 'princejetro123@gmail.com'
#     # for  adeguyijepphthah password = "olyg kany wqzi gnwf"
#     password = "iatu bier ypec yeqq"
#     subject = "You have Successfully registered for the Web Development Class"
#     body = f"""
# Dear {data['full_name']},
# Thank you for registering for the Web Development class with PrinceJetro Web Dev Training! We're excited to have you onboard.

# We want to inform you that the training program will begin on Saturday, August 31, 2024. The first class will be an Introduction to Web Development, covering topics such as:

# **Overview:**
# This class will provide a basic introduction to web development, covering:
# - What is web development?
# - Key concepts to know
# - Essential applications to install
# - Real-world applications of web development
# - Programming languages involved
# - Various frameworks

# **Topics to be Covered:**
# 1. **What is Web Development?**
#     - Definition and explanation
#     - Importance and relevance
# 2. **Key Concepts to Know**
#     - Basic terminology
#     - Fundamentals of web development
# 3. **Essential Applications to Install**
#     - Text editors/IDEs
#     - Browsers and developer tools
#     - Version control systems
# 4. **Real-World Applications of Web Development**
#     - Examples of web applications
#     - Industries and use cases
# 5. **Programming Languages Involved**
#     - HTML/CSS
#     - JavaScript
#     - Server-side languages (e.g., PHP, Python, Ruby)
# 6. **Various Frameworks**
#     - Front-end frameworks (e.g., React, Angular, Vue)
#     - Back-end frameworks (e.g., Node.js, Django, Ruby on Rails)

# Please feel free to start making the necessary preparations. If you have any questions or need assistance, reach out to us at princejetro123@gmail.com or call Jephthah Adegbuyi at +2348088981691.

# We look forward to embarking on this learning journey with you!
# Stay tuned for further information

# Best regards,
# PrinceJetro Web Development Training
# """

#     # Send the email
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#         smtp.login(sender_email, password)
#         smtp.sendmail(sender_email, email, f"Subject: {subject}\n\n{body}")

#     return Response(serializer.data)



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








from rest_framework.decorators import api_view
from rest_framework.response import Response
import smtplib, ssl

@api_view(["POST"])
def send_contact_email(request):
    data = request.data
    email = data.get("email")
    full_name = data.get("full_name")
    phone = data.get("phone")
    message = data.get("more")
    
    if not email or not full_name or not phone or not message:
        return Response({"error": "All fields are required"}, status=400)

    # Email content
    sender_email = 'princejetro123@gmail.com'
    recipient_email = 'olanikedairocentre@gmail.com'
    password = "iatu bier ypec yeqq"
    subject = "New Contact Request from School Website"
    body = f"""
Hello Olanike Dairo Administration Team,

A new contact request has been submitted through the website form. Below are the details provided by the user:

Full Name: {full_name}

Phone Number: {phone}

Email Address: {email}

Message:
{message}

Please reach out to this individual at your earliest convenience to assist with their inquiry. Thank you for your attention to this request.

Best regards,  
Automated Form Submission System, PrinceJetro Web Dev Team
"""

    # Send the email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{body}")
        return Response({"success": "Email sent successfully"})
    except Exception as e:
        return Response({"error": f"Failed to send email: {e}"}, status=500)






































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



# Example Django views.py for your blog API

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostListSerializer

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True)
    lookup_field = 'slug'  # Use slug instead of id for URLs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostSerializer
    
    def get_queryset(self):
        """Filter queryset based on action"""
        queryset = super().get_queryset()
        
        # For list view, exclude content to reduce payload
        if self.action == 'list':
            return queryset.only(
                'id', 'title', 'slug', 'excerpt', 'image_src', 'image_alt',
                'published_date', 'read_time', 'tags', 'is_published'
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured blog posts"""
        featured_posts = self.get_queryset().filter(is_featured=True)
        serializer = BlogPostListSerializer(featured_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent blog posts"""
        recent_posts = self.get_queryset().order_by('-published_date')[:5]
        serializer = BlogPostListSerializer(recent_posts, many=True)
        return Response(serializer.data)

# Alternative: Function-based views if you prefer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def blog_post_list(request):
    """Get list of blog posts (without full content)"""
    posts = BlogPost.objects.filter(is_published=True).only(
        'id', 'title', 'slug', 'excerpt', 'image_src', 'image_alt',
        'published_date', 'read_time', 'tags'
    )
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def blog_post_detail(request, slug):
    """Get single blog post with full content"""
    try:
        post = BlogPost.objects.get(slug=slug, is_published=True)
        serializer = BlogPostSerializer(post)
        return Response(serializer.data)
    except BlogPost.DoesNotExist:
        return Response(
            {'error': 'Blog post not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )