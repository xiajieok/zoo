from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from cow import models
import cow.asset_handle as asset_handle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate


# Create your views here.


def pages(request, q_all, num):
    '''
    分页功能实现,根据SQL查询内容,设定分多少页,输出
    :param request:
    :param blog_all:
    :return:
    '''
    paginator = Paginator(q_all, num)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return posts
def acc_login(request):
    '''
    登录,如果没有登录就先登录
    :param request:
    :return:
    '''
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            # pass authentication
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next') or '/')
        else:
            login_err = "Wrong username or password!"
            print('---else request-->', request)
            return render(request, 'login.html', {'login_err': login_err})
    return render(request, 'login.html')


def acc_logout(request):
    '''
    退出,返回到首页
    :param request:
    :return:
    '''
    logout(request)
    return HttpResponseRedirect('/blog')

def index(resquest):
    return render(resquest, 'index.html')


def asset_list(request):
    if request.method == 'GET':
        assets = asset_handle.fetch_asset_list()
        print(assets)
        obj = models.Asset.objects.all()
        data = pages(request, obj, 10)
        print(obj)
        return render(request, 'assets/asset.html', {'assets': assets, 'posts': data})


def asset_detail(request, asset_id):
    if request.method == 'GET':
        try:
            asset_obj = models.Asset.objects.get(id=asset_id)
            pass
        except  ObjectDoesNotExist as e:
            print(e)
            pass
        return render(request, 'assets/asset_detail.html', {'asset_obj': asset_obj})

    pass


def asset_category(request):
    type = request.GET.get('category_type')
    print(type)

    return render(request, 'assets/asset_category.html', {'type': type})
