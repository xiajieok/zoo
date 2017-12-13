from django.shortcuts import render, HttpResponse
from cow import models
import cow.asset_handle as asset_handle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


def index(resquest):
    return render(resquest, 'index.html')


def asset_list(request):
    if request.method == 'GET':
        assets = asset_handle.fetch_asset_list()
        # print(assets)
        obj = models.Asset.objects.all()
        data = pages(request, obj, 10)
        print(obj)
        return render(request, 'assets/asset.html', {'assets': assets, 'posts': data})


def asset_category(request):

    pass
