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
    # msgs = ""
    # status = ""
    if ('topic_name' in request.GET and request.GET['topic_name'] != '0'):
        # if db.status(request) == 0:
        #     status = "using cash"
        # else:
        #     status = "without cash"

        # start_time = time.time()
        blogs_list = db.getBlogsByTopic(request)
        # time_res = time.time() - start_time
        # msgs = str(time_res)
    else:
        blogs_list = db.getAllBlogs()

    paginator = Paginator(blogs_list, 30)  # Show per page
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'blogs_page.html', {'blogs': blogs})

    # return render(request, 'blogs_page.html', {'blogs': blogs_list})

def load_blog(request, id):
    blog = db.getBlog(id)

    return render(request, 'blog_post.html', {'blog': blog})

def add_blog(request):
    if request.method == 'POST':
            print request.POST['blog_name']
            print request.POST['text']
            print request.POST['topic_name']
            db.saveBlog({'name': request.POST['blog_name'], 'text': request.POST['text'], 'topic': request.POST['topic_name']})
            return redirect('/blogs/')
    elif request.method == 'GET':
       return render(request, 'add_page.html')

def remove_post(request,id):
    db.removeBlog(id)
    return redirect('/')
