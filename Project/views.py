from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from sql_lib import SQLBase

sqlDB = SQLBase()

def header(request):
    return render(request, 'header.html')

def main_page(request):
    return render(request, 'main_page.html')

def register_page(request):
    print "registration"
    if request.method == 'POST':
        print "Creating user"
        sqlDB.Create_User({'login': request.POST['login'], 'email': request.POST['email'], 'password': request.POST['password'], 'name': request.POST['name'], 'surname': request.POST['surname']})

        return redirect('/')

    return render(request,'register_page.html')

def login_page(request):
    print "logining"
    if request.method== 'POST':
        return redirect('/')

    return render(request, 'login_page.html')

def materials_page(request):
    return render(request, 'materials_page.html')