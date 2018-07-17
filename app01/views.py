from django.shortcuts import render,redirect,HttpResponse
from utils.mypage import Page
from datetime import datetime
# Create your views here.
from app01 import models
import json
from django.views.decorators.csrf import csrf_exempt
from functools import wraps

def check_login(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        ret = request.session.get('is_login')
        if ret == '1':
            return func(request,*args,**kwargs)
        else:
            next_url = request.path_info
            if request.is_ajax():
                return HttpResponse(json.dumps('a'))
            else:
                return redirect('/login/?next={}'.format(next_url))
    return inner

@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        passwd = request.POST.get('passwd')
        next_url = request.GET.get('next')
        user_obj = models.UserInfo.objects.filter(user=user,passwd=passwd).first()
        if user_obj:
            if next_url:
                rep = redirect(next_url)
            else:
                rep = redirect('/book_list/')
            request.session['is_login'] = '1'
            request.session['name'] = user
            request.session['login_time'] = str(user_obj.login_time)
            request.session.set_expiry(600)
            models.UserInfo.objects.filter(user=user, passwd=passwd).update(login_time=datetime.now().strftime("%Y-%m-%d %X"))
            return rep
    return render(request,'login.html')

from django import forms
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
class Reg(forms.Form):
    name = forms.CharField(
        min_length=4,
        max_length=16,
        label='用户名',
        error_messages={
            "required": "该字段不能为空",
        },
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )

    pwd = forms.CharField(
        label="密码",
        min_length=6,
        max_length=10,
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码不能少于6位！",
            "max_length": "密码最长10位！",
            "required": "该字段不能为空",
        }
    )

    re_pwd = forms.CharField(
        label="确认密码",
        min_length=6,
        max_length=10,
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码不能少于6位！",
            "max_length": "密码最长10位！",
            "required": "该字段不能为空",
        }
    )

    email = forms.EmailField(
        label="邮箱",
        widget=widgets.EmailInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "该字段不能为空",
            "invalid": "格式错误",
        }
    )

    phone = forms.CharField(
        label="手机",
        # 自己定制校验规则
        validators=[
            RegexValidator(r'^[0-9]+$', '手机号必须是数字'),
            RegexValidator(r'^1[3-9][0-9]{9}$', '手机格式有误')
        ],
        widget=widgets.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "该字段不能为空",
        }
    )
    def clean_name(self):
        val=self.cleaned_data.get("name")
        if not models.UserInfo.objects.filter(user=val).first():
            return val
        else:
            raise ValidationError("用户名已经注册")

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd and re_pwd and pwd!=re_pwd:
            self.add_error("re_pwd", ValidationError("两次密码不一致"))
            raise ValidationError('两次密码不一致')
        else:
            return self.cleaned_data

def register(request):
    from_obj = Reg()
    if request.method == 'POST':
        from_obj = Reg(request.POST)
        if from_obj.is_valid():
            obj = from_obj.cleaned_data
            new_obj = models.UserInfo.objects.create(user=obj['name'],passwd=obj['pwd'],login_time=datetime.now().strftime("%Y-%m-%d %X"))
            request.session['is_login'] = '1'
            request.session['name'] = obj['name']
            # request.session['login_time'] = str(new_obj.login_time)
            request.session.set_expiry(600)
            return redirect('book_list')
    return render(request,'register.html',{'from_obj':from_obj})


@check_login
def publisher_list(request):
    # 从URL取参数
    page_num = request.GET.get("page")
    # 总数据是多少
    total_count = models.Publisher.objects.all().count()
    page_obj = Page(page_num, total_count, per_page=10, url_prefix="publisher_list", max_page=11, )
    ret = models.Publisher.objects.all()[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()
    # ret = models.Publisher.objects.all().order_by('id')
    return render(request,'publisher_list.html',{'publisher_list':ret,'page_html':page_html})
@check_login
def add_publisher(request):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_city = request.POST.get('city')
        models.Publisher.objects.create(name=new_name,city=new_city)
        return redirect('publisher_list')
    return render(request,'add_publisher.html')
@check_login
def delete_publisher(request,del_id):
    models.Publisher.objects.filter(id=del_id).delete()
    return HttpResponse('ok')
@check_login
def edit_publisher(request,ed_id):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_city = request.POST.get('city')
        models.Publisher.objects.filter(id=ed_id).update(name=new_name,city=new_city)
        return redirect('publisher_list')
    edit_obj = models.Publisher.objects.filter(id=ed_id).first()
    return render(request,'edit_publisher.html',{'publisher':edit_obj})
@check_login
def book_list(request):
    # 从URL取参数
    page_num = request.GET.get("page")
    # 总数据是多少
    total_count = models.Book.objects.all().count()
    page_obj = Page(page_num, total_count, per_page=10, url_prefix="book_list", max_page=11, )
    ret = models.Book.objects.all()[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()
    # ret = models.Book.objects.all().order_by('id')
    return render(request,'book_list.html',{'book_list':ret,'page_html':page_html})
@check_login
def add_book(request):
    if request.method == 'POST':
        print(request.POST)
        new_title = request.POST.get('title')
        new_publish_date = request.POST.get('publish_date')
        new_price = request.POST.get('price')
        new_memo = request.POST.get('memo')
        new_publisher_id = request.POST.get('publisher')
        authors = request.POST.getlist('authors')
        new_book_obj = models.Book.objects.create(title=new_title,
                                                  publish_date=new_publish_date,
                                                  price=new_price,
                                                  memo=new_memo,
                                                  publisher_id=new_publisher_id)
        new_book_obj.authors.set(authors)
        return redirect('book_list')
    ret = models.Publisher.objects.all().order_by('id')
    ret1 = models.Author.objects.all().order_by('id')
    return render(request,'add_book.html',{'publisher_list':ret,
                                           'author_list':ret1})
@check_login
def delete_book(request,del_id):
    models.Book.objects.filter(id=del_id).delete()
    return HttpResponse('ok')
@check_login
def edit_book(request,ed_id):
    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_publish_date = request.POST.get('publish_date')
        new_price = request.POST.get('price')
        new_memo = request.POST.get('memo')
        new_publisher_id = request.POST.get('publisher')
        authors = request.POST.getlist('authors')
        new_book_obj = models.Book.objects.filter(id=ed_id).first()
        models.Book.objects.filter(id=ed_id).update(title=new_title,
                                                    publish_date=new_publish_date,
                                                    price=new_price,
                                                    memo=new_memo,
                                                    publisher_id=new_publisher_id)
        new_book_obj.authors.set(authors)
        return redirect('book_list')
    edit_obj = models.Book.objects.filter(id=ed_id).first()
    ret = models.Publisher.objects.all().order_by('id')
    ret1 = models.Author.objects.all().order_by('id')
    return render(request,'edit_book.html',{'book_obj':edit_obj,
                                            'publisher_list':ret,
                                            'author_list':ret1})
@check_login
def author_list(request):
    # 从URL取参数
    page_num = request.GET.get("page")
    # 总数据是多少
    total_count = models.Author.objects.all().count()
    page_obj = Page(page_num, total_count, per_page=10, url_prefix="author_list", max_page=11, )
    ret = models.Author.objects.all()[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()
    # ret = models.Author.objects.all().order_by('id')
    ret1 = models.AuthorDetail.objects.all().order_by('id')
    return render(request,'author_list.html',{'author_list':ret,
                                              'authordetail_list':ret1,
                                              'page_html':page_html})
@check_login
def add_author(request):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_books = request.POST.getlist('books')
        new_age = request.POST.get('age')
        new_phone = request.POST.get('phone')
        new_address = request.POST.get('address')
        new_email = request.POST.get('email1')
        ad_obj = models.AuthorDetail.objects.create(address=new_address,
                                                    author_email=new_email)
        new_books_obj = models.Author.objects.create(name=new_name,
                                                     age=new_age,
                                                     phone=new_phone,
                                                     detail_id=ad_obj.id)
        new_books_obj.book_set.set(new_books)
        return redirect('author_list')
    ret = models.Book.objects.all().order_by('id')
    return render(request,'add_author.html',{'book_list':ret})
@check_login
def delete_author(request,del_id):
    models.AuthorDetail.objects.filter(id=models.Author.objects.get(id=del_id).detail_id).delete()
    models.Author.objects.filter(id=del_id).delete()
    return HttpResponse('ok')
@check_login
def edit_author(request,ed_id):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_books = request.POST.getlist('books')
        new_age = request.POST.get('age')
        new_phone = request.POST.get('phone')
        new_books_obj = models.Author.objects.filter(id=ed_id).first()
        new_books_obj.book_set.set(new_books)
        ad = models.Author.objects.get(id=ed_id).detail_id
        new_auth_address = request.POST.get('address')
        new_auth_email = request.POST.get('email1')
        models.Author.objects.filter(id=ed_id).update(name=new_name,
                                                      age=new_age,
                                                      phone=new_phone,
                                                      )
        models.AuthorDetail.objects.filter(id=ad).update(address=new_auth_address,
                                                         author_email=new_auth_email)


        return redirect('author_list')
    author_obj = models.Author.objects.filter(id=ed_id).first()
    ret = models.Book.objects.all().order_by('id')
    return render(request,'edit_author.html',{'author_obj':author_obj,
                                              'book_list':ret})

def logout(request):
    request.session.flush()
    return redirect('/login/')