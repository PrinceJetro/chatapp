from .views import *
from django.urls import path

urlpatterns = [
    path('', getRoutes, name='register'),
    path('all', getAll, name='all'),
    path('create', createComplaint, name='create'),
    path('student', send_contact_email, name='student'),
]
