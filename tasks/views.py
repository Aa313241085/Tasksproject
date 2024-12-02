from django.shortcuts import render, redirect
from tasks.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

@csrf_exempt
def create_user(request):
    if request.method == 'GET':
        return render(request, template_name='create_user.html')
    if request.method == 'POST':
        try:
            username=request.POST['username']
            password=request.POST['password']
            is_admin=request.POST['is_admin']
            try:
              username_exist = User.objects.get(username=username)
              if username_exist:
                return render(request, "create_user.html", {'message': 'Username already exist.'})
            except User.DoesNotExist:
                pass
            
            user= User(username=username, password=password,is_admin=is_admin)
            user.save()
            return redirect('home')
        
        except:
            return render(request, "create_user.html", {'message': 'General error. Please try again later'})

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request=request, template_name="login.html")
    
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
    
            user_exist = User.objects.get(username=username, password=password)

            if user_exist:
              request.session["auth"] = {'username': user_exist.username, 'is_admin': user_exist.is_admin}
              return redirect('home')

            return render(request, "login.html", {'message': 'Invalid username and/or password. Please try again'})
        except User.DoesNotExist:
            return render(request, "login.html", {'message': 'Invalid username and/or password. Please try again'})
        except:
            return render(request, "login.html", {'message': 'General error. Please try again later'})


def logout(request):
    try:
        del request.session["auth"]
    except KeyError:
        pass
    return redirect('login')

def home(request):
    try:
        if not is_login(request):
            return redirect('login')
        user=get_user(request)
        sharedTasks=[]
        if user.is_admin:
            tasks = Task.objects.all()
        else:    
            tasks = Task.objects.filter(user=user)
            sharedTasks=SharedTask.objects.filter(user=user)
            
        return render(request, "home.html", {"tasks" : tasks, "sharedTasks": sharedTasks})
    except:
       return render(request, "home.html", {"tasks" : [], 'message': 'General error. please try again later'})


@csrf_exempt
def create_task(request):
    if not is_login(request):
        return redirect('login')
    
    if request.method == 'POST':
        client=request.POST["client"]
        category=request.POST["category"]
        description=request.POST["description"]
        Task(
            user = get_user(request),
            client = client,
            category = category,
            description = description
        ).save()
        return redirect('home')
    
    return render(request, "create_task.html", {'clients': Task.Client, 'categories': Task.Category})

def get_user(request):
    return User.objects.get(username=request.session['auth']['username'])

def is_login(request):
    user_session = request.session.get('auth', False)

    if not user_session:
        return False

    return True

@csrf_exempt
def delete(request, id):
    try:
        if not is_login(request):
            return redirect('login')
        Task.objects.get(id=id).delete()
        
        return redirect('home')
    except Exception as ex:
        print(ex)
        #render error.html
        pass
        
def update(request, id):
    if not is_login(request):
        return redirect('login')
    task = Task.objects.get(id=id)
    
    if request.method == 'GET':
       users=User.objects.filter(~Q(username=get_user(request).username) & ~Q(username=task.user.username)).values('username').distinct()
       sharedTask=None
       try:
         sharedTask=SharedTask.objects.get(task__id=id).user.username
       except SharedTask.DoesNotExist:
           pass  
       
       return render(request,"update.html",{"task":task, "categories":Task.Category, 'clients': Task.Client, 'users': users, 'sharedTask': sharedTask})
    if request.method == 'POST':
       client = request.POST['client']
       category = request.POST['category']
       description = request.POST['description']
       sharedTask=request.POST['sharedTask']
       try:
           user=User.objects.get(username=sharedTask)
           existing_shared_task = SharedTask.objects.filter(user=user, task=task)
           if len(existing_shared_task) > 0:
               pass
           else:
               SharedTask.objects.filter(task=task).delete()
               shared_task=SharedTask(user=user,task=task)
               shared_task.save()
       except User.DoesNotExist:
           SharedTask.objects.filter(task=task).delete()
       
       task.client = client
       task.category = category
       task.description = description
       task.save()
       return redirect("home")

def search(request):
    q = request.GET["q"]
    tasks = Task.objects.filter(Q(client__contains=q) | Q(description__contains=q) | Q(category__contains=q))  
    return render(request, "home.html", {"tasks": tasks})

def show_user(request):
    if not is_login(request):
        return redirect('login')

    user = get_user(request)

    if user.is_admin:
        users = User.objects.all()

        return render(request, "show_user.html", {"users": users})

    return render(request, "show_user.html")

@csrf_exempt
def delete_user(request,id):
    try:
        if not is_login(request):
            return redirect('login')
        User.objects.get(id=id).delete()
        
        return redirect('home')
    except Exception as ex:
        print(ex)
        #render error.html
        pass