from django.db import models

# Create your models here.
class Teacher(models.Model):
    account = models.CharField(max_length =100)
    name = models.CharField(max_length =100)
    headimg = models.CharField(max_length=300,default="")
    phone = models.CharField(max_length =30,default="")
    intro = models.CharField(max_length=500)
    add_time = models.DateField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    class Meta:
        db_table = 'teacher'
    def __str__(self):
        return self.name
