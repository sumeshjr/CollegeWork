
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('goals/', goals, name="goals"),
    path('index/', index, name="index"),
    path('contact/', contact, name="contact"),
    path('registerAdmin/', registerAdmin, name="registerAdmin"),
    path('loginAdmin/', loginAdmin, name="loginAdmin"),
    path('about/', about, name="about"),
    path('task_list/<int:task_id>/', task_list, name='task_list'),
    path('dashboard/', dashboard, name='dashboard'),
    path('addTask/', addTask, name='addTask'),
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    path('update_password/', update_password, name='update_password'),
    path('signout/', signout, name="signout"),
    path('update_user/<int:user_id>/', update_user_view, name='updateUser'),
    path('add_goal/', add_goal, name='add_goal'),
    path('update_goal/<int:goal_id>/', update_goal, name='update_goal'),
    path('delete_goal/<int:goal_id>/', delete_goal, name='delete_goal'),
    path('delete_user/', delete_user, name="delete_user"),
    path('completed_goals/', completed_goals, name="completed_goals"),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    path('users/<int:user_id>/', view_single_user, name='view_single_user'),
    path('view-users/', viewUsers, name='view_users'),
    path('view-tasks/', viewTasks, name='view_tasks'),
    path('view-contacts/', view_contacts, name='view_contacts'),
    path('view-goals/', viewGoals, name='view_goals'),
    path('create-task/', create_task, name='create_task'),
    path('update-task/<int:task_id>/', update_task, name='update_task'),
    path('delete-task/<int:task_id>/', delete_task, name='delete_task'),
    path('forgot_password/', forgot_password, name='forgot_password'), 
    path('create/', create_blog, name='create_blog'),
    path('update/<int:blog_id>/', update_blog, name='update_blog'),
    path('delete/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('blog_list/', blog_list, name='blog_list'),
    path('reset_password/<str:uidb64>/<str:token>/', reset_password, name='reset_password'),
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

