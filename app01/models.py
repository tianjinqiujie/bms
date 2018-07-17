from django.db import models

# Create your models here.
from django.db import models
# Create your models here.
# 书
class Book(models.Model):
    title = models.CharField(max_length=32)
    publish_date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    memo = models.TextField(null=True)
    # 创建外键，关联publish
    publisher = models.ForeignKey(to="Publisher",on_delete=models.CASCADE)
    # 创建多对多关联author
    authors = models.ManyToManyField(to="Author")

    def __str__(self):
        return self.title


# 出版社
class Publisher(models.Model):
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)

    def __str__(self):
        return self.name


# 作者
class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    phone = models.CharField(max_length=11)
    detail = models.OneToOneField(to="AuthorDetail",on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# 作者详情
class AuthorDetail(models.Model):
    address = models.CharField(max_length=64)
    author_email = models.EmailField()


class UserInfo(models.Model):
    user = models.CharField(max_length=32)
    passwd = models.CharField(max_length=32)
    login_time = models.DateTimeField(null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(null=True,max_length=12)