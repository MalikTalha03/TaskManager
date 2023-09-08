from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from task_manager.models import UserData
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator


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


# Other imports as needed

def update_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if new password and confirmation match
        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)  # Set the new password
                user.save()  # Save the updated user

                # Optionally, you can log the user in automatically
                authenticated_user = authenticate(request, username=user.username, password=new_password)
                if authenticated_user is not None:
                    login(request, authenticated_user)

                # Redirect to a success page or show a success message
                return redirect(dashboard)
            except User.DoesNotExist:
                # User with this email does not exist
                messages.error(request, 'No user with this email address exists.')
        else:
            # Passwords do not match
            messages.error(request, 'Passwords do not match.')

    # If the request method is GET, render the password update form.
    return render(request, "update_password.html")

# views.py



@login_required
def my_profile(request):
    # Get the user's name and email
    full_name = request.user.first_name + ' ' + request.user.last_name
    user_email = request.user.email
    user_name = request.user.username
    

    # Calculate the total tasks
    total_completed_tasks = UserData.objects.filter(status='Completed', user=request.user).count()
    total_pending_tasks = UserData.objects.filter(status='Pending', user=request.user).count()
    total_todo_tasks = UserData.objects.filter(status='None', user=request.user).count()

    return render(request, 'my_profile.html', {
        'full_name': full_name,
        'user_email': user_email,
        'total_completed_tasks': total_completed_tasks,
        'total_pending_tasks': total_pending_tasks,
        'total_todo_tasks': total_todo_tasks,
        'user_name' : user_name,
    })

@login_required
def update_profile(request):
    # Get the user's name and email
    first_name = request.user.first_name 
    user_name = request.user.username
    last_name = request.user.last_name 
    user_email = request.user.email 

    if request.method == 'POST':
        updated_first_name=request.POST.get('first_name')
        updated_last_name=request.POST.get('last_name')
        updated_email=request.POST.get('email')
        user = User.objects.get(username=request.user.username)
        user.first_name = updated_first_name
        user.last_name = updated_last_name
        user.email = updated_email
        user.save()
        
        # Redirect or display a success message after handling the form data
        return redirect( 'dashboard')

    return render(request, 'update_profile.html', {
        'first_name': first_name,
        'user_email': user_email,
        'user_name': user_name,
        'last_name': last_name,
    })