from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50,null=True,blank=True)
    phone = models.CharField(max_length=50,null=True,blank=True)
    class Meta:
        db_table = 'user'
    def __str__(self):
        return self.username

class Student(models.Model):
    no = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50,unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    number = models.IntegerField(default=999)
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    class Meta:
        db_table = 'student'
    def __str__(self):
        return self.name