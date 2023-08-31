from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from task_manager.models import UserData
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.hashers import make_password

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('dashboard')
    
    return render(request, "registration.html")
    

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('dashboard')
            else:
                error_message = 'Invalid credentials'
                messages.error(request, error_message)
        else:
            error_message = 'User does not exist'
            messages.error(request, error_message)

    next_url = request.GET.get('next')

    context = {'next_url': next_url}
    return render(request, "login.html", context)



def dashboard(request):
    if request.user.is_authenticated:
        user_data = UserData.objects.filter(user=request.user)
    
        todo_tasks = user_data.filter(status='None')
        pending_tasks = user_data.filter(status='Pending')
        completed_tasks = user_data.filter(status='Completed')
        user_name = "Welcome " + request.user.username
        context = {
            'todo_tasks': todo_tasks,
            'pending_tasks': pending_tasks,
            'completed_tasks': completed_tasks,
            'user_name': user_name,
        }
        
        return render(request, "dashboard.html", context)
    else:
        return render(request, "login.html")



@login_required
def addtask(request):
    if request.method == "POST":
        # Fetch data from the HTML form
        task = request.POST['title']
        description = request.POST['description']
        completion_date_str = request.POST['date']  # Get the completion date from the form input
        status = "None"
        completion_date = datetime.strptime(completion_date_str, '%Y-%m-%d').date()  # Convert the string to a date object
        current_date = datetime.now().date()  # Get the current date

        # Create a new UserData object and save it
        user_data = UserData(user=request.user, task=task, description=description, date=current_date, status=status, completion_date=completion_date)
        user_data.save()

        return redirect('dashboard')
    
    return render(request, "add_task.html")

def user_logout(request):
    logout(request)
    return redirect('login') 

from django.http import JsonResponse

def update_task_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        try:
            task = UserData.objects.get(pk=task_id, user=request.user)
            if task.status == 'None':
                task.status = 'Pending'
            elif task.status == 'Pending':
                task.status = 'Completed'
            task.save()
            return JsonResponse({'success': True})
        except UserData.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found or not authorized.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
