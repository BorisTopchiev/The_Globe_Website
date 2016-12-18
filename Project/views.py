from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from sql_lib import SQLBase
from mongomanager import DataBase
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

sqlDB = SQLBase()
db = DataBase()
def header(request):
    return render(request, 'header.html')

def main_page(request):
    return render(request, 'main_page.html')

def register_page(request):
    print "registration"
    if request.method == 'POST':
        print "Creating user"
        sqlDB.Create_User({'login': request.POST['login'], 'email': request.POST['email'], 'password': request.POST['password'], 'name': request.POST['name'], 'surname': request.POST['surname']})
        db.saveUser({'login': request.POST['login'], 'email': request.POST['email'], 'name': request.POST['name'], 'surname': request.POST['surname']})
        return redirect('/')

    return render(request, 'register_page.html')

def login_page(request):
    print "logining"
    if request.method== 'POST':
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')

    return render(request, 'login_page.html')

def materials_page(request):
    return render(request, 'materials_page.html')

def blogs_page(request):


    blogs_list = db.getAllBlogs()

    # paginator = Paginator(blogs_list, 30)  # Show per page
    # page = request.GET.get('page')
    # try:
    #     blogs = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     blogs = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     blogs = paginator.page(paginator.num_pages)

    return render(request, 'blogs_page.html', {'blogs': blogs_list[0:20]})

    # return render(request, 'blogs_page.html', {'blogs': blogs_list})