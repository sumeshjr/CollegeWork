from django.db import models
from django.contrib.auth.models import User

class Register_table(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.EmailField(max_length=255,null=True)
    contact_number = models.IntegerField()
    password = models.CharField(max_length=200)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True, default="Male")
    added_on = models.DateField(auto_now_add=True, null=True, blank=True)
    uploaded_on = models.DateField(auto_now_add=True, null=True, blank=True)
    

    def __str__(self):
        return str(self.user.username)
    

class Goals(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    images = models.ImageField(upload_to="goal_images", null=True, blank=True)
    
    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    images = models.FileField(upload_to="task_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False) 

    def __str__(self):
        return self.title

class UserTaskImage(models.Model):
    user = models.ForeignKey(Register_table, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_image = models.ImageField(upload_to="user_completed_images", null=True, blank=True , default=False)
    is_completed = models.BooleanField(default=False) 
    date_uploaded = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"User: {self.user.user.username} - Task: {self.task.title}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.EmailField(max_length=255)
    password = models.CharField(max_length=200,default="",null=True)
    
    def __str__(self):
        return self.username
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author=models.TextField()

    def __str__(self):
        return self.title
    


