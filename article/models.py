from django.db import models

# Create your models here.
class People(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'people'
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    cover = models.CharField(max_length=300,null=True,blank=True)
    intro = models.CharField(max_length=300,null=True,blank=True)
    people = models.ForeignKey(People,on_delete=models.CASCADE, related_name='article')
    content = models.CharField(max_length=500,null=True,blank=True)
    add_time = models.DateField(auto_now_add=True,null=True,blank=True)
    disable = models.BooleanField(default=False,verbose_name="是否禁用")
    is_delete = models.BooleanField(default=False,verbose_name="是否删除")
    class Meta:
        db_table = 'article'
    def __str__(self):
        return self.title