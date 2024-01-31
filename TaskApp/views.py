
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sessions.backends.db import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Register_table
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes



def index(request):
    blogs=Blog.objects.all()
    return render(request,'homepage_1.html',{"blogs":blogs})

def about(request):
    return render(request,'aboutus.html')

@login_required
def task_list(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user = request.user
    try:
        user_task_image = UserTaskImage.objects.get(user=user.register_table, task=task)
        is_completed = user_task_image.is_completed
    except UserTaskImage.DoesNotExist:
        is_completed = False

    com = UserTaskImage.objects.all()
    context = {'user': user, 'task': task, 'com': com, 'is_completed': is_completed}
    return render(request, 'task.html', context)

@login_required
def completed_goals(request, user_id):
    completed_tasks = UserTaskImage.objects.filter(user__id=user_id, is_completed=True)

    context = {
        'completed_tasks': completed_tasks,
    }

    return render(request, 'completed_goals.html', context)


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user = request.user.register_table

    if request.method == 'POST':
        try:
            user_task_image = UserTaskImage.objects.get(user=user, task=task)
        except UserTaskImage.DoesNotExist:
            user_task_image = UserTaskImage.objects.create(user=user, task=task)

        completed_image = request.FILES.get('completed_image')

        if completed_image:
            if user_task_image.completed_image:
                # If a file already exists, update it with the new file
                user_task_image.completed_image.delete()  # Delete the old file
            user_task_image.completed_image = completed_image
            user_task_image.is_completed = True  # Set is_completed to True when the image is uploaded
            user_task_image.save()

            # Mark the task as completed
            task.completed = True
            task.save()

            messages.success(request, f'Task "{task.title}" completed successfully!')
        else:
            messages.warning(request, 'Please upload a completed image.')

        return redirect('/goals', task_id=task.id)

    # Handle cases where the request method is not POST
    return render(request, 'goals.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        password = request.POST['password']
        age = request.POST.get('age', None)
        gender = request.POST.get('gender', 'Male')

        # Check if the username (email) already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Username already exists')

            # Username (email) already exists, you can handle this case (e.g., show an error message)
            return render(request, 'Login.html', {'error_message': 'Username already exists'})

        # Username is unique, create User and Register_table instances
        user = User.objects.create_user(username=email, password=password)
        register_table = Register_table(user=user, username=email, contact_number=contact_number, password=password, age=age, gender=gender)
        register_table.save()

        # Authenticate and log in the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/index')  # Redirect to the home page or any other desired page

    return render(request, 'Login.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/index')  # Redirect to the home page or any other desired page
        else:
            # Handle invalid login
            return render(request, 'Login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'Login.html')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(username=email).first()

        if user is not None:
            # Generate a password reset token
            token = default_token_generator.make_token(user)

            # Build the password reset URL
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = reverse('reset_password', kwargs={'uidb64': uidb64, 'token': token})
            reset_url = request.build_absolute_uri(reset_url)

            # Send a password reset email
            subject = 'Reset Your Password'
            message = f'Click the following link to reset your password: {reset_url}'
            from_email = 'example@gmail.com'  # Replace with your email address
            to_email = [user.email]
            
            send_mail(subject, message, from_email, to_email)

            # Inform the user about the email
            messages.success(request, 'Password reset email sent successfully. Check your inbox.')
            return render(request, 'forgot_password_success.html')

    return render(request, 'forgot.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()

            # Log in the user after password reset
            authenticated_user = authenticate(request, username=user.username, password=new_password)
            login(request, authenticated_user)

            messages.success(request, 'Password successfully reset. You are now logged in.')
            return redirect('/index')  # Redirect to the home page or any other desired page

        return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'Invalid password reset link. Please try again.')
        return render(request, 'login.html') 

@login_required
def update_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            # Check if the user is authenticated
            if request.user.is_authenticated:
                # Update the user's password
                request.user.set_password(new_password)
                request.user.save()

                # Update the user's session to reflect the new password
                update_session_auth_hash(request, request.user)

                messages.success(request, 'Password updated successfully.')
                return redirect('/index')  # Redirect to the home page or any other desired page
            else:
                messages.error(request, 'User not authenticated.')
                return redirect('/signin')  # Redirect to the login page
        else:
            messages.error(request, 'Password and Confirm Password do not match.')
            return redirect('update_password')

    return render(request, 'update_password.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')

@login_required
def goals(request):
    all_goals = Goals.objects.all()
    goals_and_tasks = []

    for goal in all_goals:
        tasks_for_goal = Task.objects.filter(goal=goal)
        goals_and_tasks.append({'goal': goal, 'tasks': tasks_for_goal})

    return render(request, 'goals.html', {'goals_and_tasks': goals_and_tasks})


def registerAdmin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Choose a different one.')
            return redirect('registerAdmin')

        # Create a new User instance (built-in Django User model)
        user = User.objects.create_user(username=username, password=password)

        # Create an associated AdminProfile instance
        admin_profile = Admin(user=user, username=username, password=password)
        admin_profile.save()

        messages.success(request, 'Account created successfully!')
        return redirect('loginAdmin')

    return render(request, 'adminregister.html')


def loginAdmin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's authenticate method to check if the username and password match
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user has an associated Admin profile
            if hasattr(user, 'admin'):
                # Use Django's login method to log in the user
                login(request, user)
                
                # Retrieve additional details from the Admin model
                admin_profile = Admin.objects.get(user=user)
                
                # You can now use admin_profile in your views
                messages.success(request, 'Login successful!')
                return redirect('dashboard')  # Replace 'dashboard' with the actual URL name for the dashboard
            else:
                messages.error(request, 'Login failed. You do not have access to the admin dashboard.')
        else:
            messages.error(request, 'Login failed. Please check your username and password.')

    return render(request, 'adminlogin.html')


@login_required
def addTask(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        goal = request.POST.get('goal')
        images = request.FILES.get('images')

        # Create a new Task instance
        task = Task(title=title, description=description, goal=goal, images=images)
        task.save()

        return redirect('/dashboard')  # Replace 'task_list' with the actual URL name for the task list page

    return render(request, 'addTask.html')
       


@login_required
def signout(request):
    logout(request)
    return render(request,'homepage_1.html')

@login_required
def completed_goals(request):
    user = request.user.register_table

    # Retrieve completed tasks for the current user
    completed_tasks = UserTaskImage.objects.filter(user=user, is_completed=True).select_related('task')

    return render(request, 'completed_goals.html', {'completed_tasks': completed_tasks})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def viewUsers(request):
    users=Register_table.objects.all()
    return render(request,'viewUsers.html' ,{"users":users})

@login_required
def viewTasks(request):
    tasks=Task.objects.all()
    return render(request,'viewTasks.html',{"tasks":tasks})

@login_required
def viewGoals(request):
    goals=Goals.objects.all()
    return render(request,'viewGoals.html',{"goals":goals})

@login_required
def view_single_user(request, user_id):
    user = get_object_or_404(Register_table, id=user_id)
    return render(request, 'view_single_user.html', {"user": user})


@login_required
def update_user_view(request, user_id):
    user = get_object_or_404(Register_table, user__id=user_id)

    if request.method == 'POST':
        # Retrieve updated values from the request
        new_contact_number = request.POST.get('contact_number')
        new_age = request.POST.get('age')
        new_gender = request.POST.get('gender')
        new_password = request.POST.get('password')

        # Update the user object with the new values
        user.contact_number = new_contact_number
        user.age = new_age
        user.gender = new_gender

        # Check if a new password is provided
        if new_password:
            # Update the password in the Register_table
            user.password = new_password
            user.save()

            # Update the password in the User table
            user_account = User.objects.get(id=user.user_id)
            user_account.set_password(new_password)
            user_account.save()

        # Redirect to viewUsers or any other appropriate page
        return redirect('/dashboard')

    return render(request, 'update_user.html', {'user': user})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user_id = request.GET.get('user_id')
        user = get_object_or_404(User, id=user_id)

        # Delete the associated Register_table instance
        register_table = user.register_table
        register_table.delete()

        # Delete the User instance
        user.delete()

        return redirect('view_users')  # Redirect to the user view or any other desired page

    return render(request, 'delete_user.html') 


@login_required
def add_goal(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image')

        goal = Goals.objects.create(title=title, description=description, images=image)
        return redirect('view_goals')  # Redirect to the goals view or any other desired page

    return render(request, 'add_goal.html')  # Replace 'add_goal.html' with the actual template name



@login_required
def update_goal(request, goal_id):
    goal = get_object_or_404(Goals, id=goal_id)

    if request.method == 'POST':
        goal.title = request.POST['title']
        goal.description = request.POST['description']
        image = request.FILES.get('image')

        if image:
            goal.images = image

        goal.save()
        return redirect('view_goals')  # Redirect to the goals view or any other desired page

    return render(request, 'update_goal.html', {'goal': goal})  # Replace 'update_goal.html' with the actual template name

@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goals, id=goal_id)

    if request.method == 'POST':
        goal.delete()
        return redirect('view_goals')  # Redirect to the goals view or any other desired page

    return render(request, 'delete_goal.html', {'goal': goal})  # Replace 'delete_goal.html' with the actual template name

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        images = request.FILES.get('images')
        goal_id = request.POST.get('goal')  # Assuming you have a select input for choosing the goal

        goal = get_object_or_404(Goals, id=goal_id)

        task = Task.objects.create(title=title, description=description, images=images, goal=goal)
        messages.success(request, 'Task created successfully!')
        return redirect('view_tasks')

    goals = Goals.objects.all()
    return render(request, 'create_task.html', {'goals': goals})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        images = request.FILES.get('images')
        if images:
            task.images = images

        goal_id = request.POST.get('goal')  # Assuming you have a select input for choosing the goal
        goal = get_object_or_404(Goals, id=goal_id)
        task.goal = goal

        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('view_tasks')

    goals = Goals.objects.all()
    return render(request, 'update_task.html', {'task': task, 'goals': goals})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('view_tasks')

    return render(request, 'delete_task.html', {'task': task})


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Blog

# Create view
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')
        
        # Validate and create the blog
        if title and description and author:
            Blog.objects.create(title=title, description=description, author=author)
            return redirect('blog_list')  # Redirect to a URL name for listing blogs
        else:
            return HttpResponse("Invalid data. All fields are required.")

    return render(request, 'create_blog.html')

# Update view
def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')
        
        # Validate and update the blog
        if title and description and author:
            blog.title = title
            blog.description = description
            blog.author = author
            blog.save()
            return redirect('blog_list')  # Redirect to a URL name for listing blogs
        else:
            return HttpResponse("Invalid data. All fields are required.")

    return render(request, 'update_blog.html', {'blog': blog})

# Delete view
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')  # Redirect to a URL name for listing blogs

    return render(request, 'delete_blog.html', {'blog': blog})

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

def view_contacts(request):
    contacts=ContactMessage.objects.all()
    return render(request,'view_contacts.html' ,{"contacts":contacts} )