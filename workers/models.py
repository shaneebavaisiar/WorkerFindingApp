
from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    dist = models.CharField(max_length=200,unique=True)
    state = models.CharField(max_length=120)
    country = models.CharField(max_length=120)

    def __str__(self):
        return self.dist


class Job(models.Model):
    job_name = models.CharField(max_length=120, unique=True)
    daily_wages = models.IntegerField()

    def __str__(self):
        return self.job_name


class Worker(models.Model):
    name = models.CharField(max_length=120, unique=True)
    choices = (
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Transgender', 'Transgender'),
        ('Non-binary', 'Non-binary'),
        ('intersex', 'intersex'),
        ('I prefer not to say', 'I prefer not to say')
    )
    gender = models.CharField(choices=choices, max_length=50, null=True)
    age = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=120)
    address = models.CharField(max_length=300)
    adhar_card = models.CharField(max_length=120, null=False)
    driving_licence = models.CharField(max_length=120, null=True)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)
    join_date = models.DateField(auto_now=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    status = (
        ("Available", "Available"),
        ("Not Available", "Not Available")

    )
    current_status = models.CharField(choices=status, null=True, max_length=20)

    def __str__(self):
        return self.name


class HireWorkers(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    customer_phone=models.CharField(max_length=12,null=True)
    choices = (
        ("Hire Worker", "Hire Worker"),

        ("Cancel worker", "Cancel worker")
    )
    hire = models.CharField(choices=choices, null=True, max_length=20)
    hire_date = models.DateField(auto_now=True)
    days = models.IntegerField(null=True)


class Feedback(models.Model):
    customer_name = models.ForeignKey(User,on_delete=models.CASCADE)
    worker_name = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
    choices = (
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Bad", "Bad")
    )
    feedback = models.CharField(choices=choices, null=True, max_length=20)
    content = models.TextField(null=True)
    date=models.DateField(auto_now=True)

    def __str__(self):
        return self.feedback

class Comment(models.Model):
  worker = models.ForeignKey(Worker, on_delete = models.CASCADE, related_name ='comments')
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  content = models.TextField(null=True)