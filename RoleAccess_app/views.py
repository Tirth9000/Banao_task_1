from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import default_storage
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.base import ContentFile
from .models import UserModel, Blogs
from Templates import *
import os

# Create your views here.
def LandingPage(request):
    return render(request, 'landing.html')

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = UserModel.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            request.session['username'] = user.username
            request.session['status'] = 'loggedin'
            print(user.role)
            if user.role == 'Dr':
                return redirect('doctor')
            else:
                return redirect('patient')
        else:
            return render(request, 'login.html', {'error': True})
    return render(request, 'login.html', {'error': False})


def UserSignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        new_user = UserModel.objects.create(
            username = username,
            password = make_password(password),
            email = email
        )
        new_user.save()
        request.session['username'] = username
        return redirect('user_register')
    return render(request, 'signup.html', {'error': False})


def CheckValidUser(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        email = request.GET.get('email')
        if username and len(username) < 8:
            return HttpResponse('<small class="username-status text-red-600 text-left">Invalid Username (i.e. "Tirth9000")</small>')
        elif UserModel.objects.filter(username=username).exists():
            return HttpResponse('<small class="username-status text-red-600 text-left">Username already taken!</small>')
        elif UserModel.objects.filter(email=email).exists():
            return HttpResponse('<small class="email-status text-red-600 text-left">User on this email already exists!</small>')
    return HttpResponse('')

def UserRegister(request):
    user_name = request.session.get('username')
    user = UserModel.objects.filter(username = user_name).first()
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.role = request.POST.get('role')
        user.address_line = request.POST.get('address_line')
        user.state = request.POST.get('state')
        user.city = request.POST.get('city')
        user.pincode = request.POST.get('pincode')
        profile_pic = request.FILES.get('profile_image')
        if profile_pic:
            file_extension = os.path.splitext(profile_pic.name)[1]  
            new_file_name = f"{user.username}_image{file_extension}" 
            file_path = default_storage.save(new_file_name, ContentFile(profile_pic.read()))
            user.profile_pic = file_path
        user.save()
        del request.session['username']
        return redirect('user_login')
    return render(request, 'register.html')


def DoctorPage(request):
    user_name = request.session.get('username')
    user = UserModel.objects.filter(username = user_name).first()
    blogs = Blogs.objects.filter(author=user)
    return render(request, 'doctor.html', {'user': user, 'blogs': blogs[::-1]})

def PatientPage(request):
    user_name = request.session.get('username')
    user = UserModel.objects.filter(username = user_name).first()
    blogs = Blogs.objects.all()
    return render(request, 'patient.html', {'user': user, 'blogs': blogs[::-1]})


def UploadBlog(request):
    user_name = request.session.get('username')
    user = UserModel.objects.filter(username = user_name).first()
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        blog_image = request.FILES.get('image')
        draft = request.POST.get('draft')

        if blog_image:
            file_extension = os.path.splitext(blog_image.name)[1]  
            new_file_name = f"{user.username}_blog{file_extension}" 
            file_path = default_storage.save(new_file_name, ContentFile(blog_image.read()))
            
            blog = Blogs.objects.create(
                author = user,
                title = title,
                category = category,
                summary = summary,
                content = content,
                blog_image = file_path,
                draft = bool(draft)
            )
            blog.save()

        return redirect('doctor')
    return redirect('doctor')