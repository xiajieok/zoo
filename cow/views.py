from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from cow import models
import cow.asset_handle as asset_handle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
import json
from client import core
from django.forms.models import model_to_dict
import datetime
from cow import core
import yaml

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
        except  ObjectDoesNotExist as e:
            print(e)
        return render(request, 'assets/asset_detail.html', {'asset_obj': asset_obj})


def asset_category(request, type):
    assets = asset_handle.fetch_asset_list(type)
    obj = models.Asset.objects.all()
    data = pages(request, obj, 10)
    print(obj)
    return render(request, 'assets/asset.html', {'assets': assets, 'posts': data})
    # return HttpResponse('hahaha')


from cow.dashboard import AssetDashboard


def get_dashboard_data(request):
    dashboard_data = AssetDashboard(request)
    dashboard_data.searilize_page()
    res = json.dumps(dashboard_data.data)
    print(res)

    return HttpResponse(res)


def asset_report(request):
    print(request.GET)
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        if ass_handler.data_is_valid():
            print("----asset data valid:")
            ass_handler.data_inject()
            # return HttpResponse(json.dumps(ass_handler.response))

        return HttpResponse(json.dumps(ass_handler.response))
        # return render(request,'assets/asset_report_test.html',{'response':ass_handler.response})
        # else:
        # return HttpResponse(json.dumps(ass_handler.response))

    return HttpResponse('--test--')


def asset_with_no_asset_id(request):
    print(request.POST)
    if request.method == 'POST':
        asset_handler = core.Asset(request)
        res = asset_handler.get_asset_id_by_sn()
        print('我是获取的SN',res)
        return HttpResponse(json.dumps(res))



    # if request.method == 'GET':
    #     print('开始获取ID')
    #     res = models.Asset.objects.order_by('-id').values('id')[0:1]
    #     next_id = int(list(res)[0]['id']) + 1
    #     return HttpResponse(next_id)
    # else:
    #     data = request.POST
    #     print(data)
    #     asset_sn = data.get('sn')
    #     asset_already_in_approval_zone = models.NewAssetApprovalZone.objects.get_or_create(sn=asset_sn,
    #                                                                                        data=json.dumps(
    #                                                                                                data),
    #                                                                                        manufactory=data.get(
    #                                                                                                'manufactory'),
    #                                                                                        model=data.get(
    #                                                                                                'model'),
    #                                                                                        asset_type=data.get(
    #                                                                                                'asset_type'),
    #                                                                                        ram_size=data.get(
    #                                                                                                'ram_size'),
    #                                                                                        cpu_model=data.get(
    #                                                                                                'cpu_model'),
    #                                                                                        cpu_count=data.get(
    #                                                                                                'cpu_count'),
    #                                                                                        cpu_core_count=data.get(
    #                                                                                                'cpu_core_count'),
    #                                                                                        os_distribution=data.get(
    #                                                                                                'os_distribution'),
    #                                                                                        os_release=data.get(
    #                                                                                                'os_release'),
    #                                                                                        os_type=data.get(
    #                                                                                                'os_type'),
    #
    #                                                                                        )
    #     print(asset_already_in_approval_zone)
    #
    # return HttpResponse('200')


def assets_approval(request):
    if request.method == 'GET':
        obj = models.NewAssetApprovalZone.objects.filter(approved=False)
        return render(request, 'assets/assets_approval.html', {'asset_data': obj})
    else:
        id_list = request.POST.getlist('ids[]')
        obj_list = models.NewAssetApprovalZone.objects.filter(id__in=id_list)

        for obj in obj_list:
            asset_handler = core.Asset(request)
            if asset_handler.data_is_valid_without_id():
                obj.approved = True
                obj.approved_date = datetime.datetime.now()
                obj.save()
            else:
                print('数据不完整')
        return HttpResponse('ok')
def cloud_node(request):
    return render(request, 'cloud/node.html')
def cloud_format(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        print(req['namespace'])
        tmp = {
            'namespace':req['namespace'],
            'AppName':req['AppName'],
            'image':req['image'],
            'replicas':req['replicas'],
            'Resources':{
                'cpu': req['cpu'],
                'mem': req['mem'],
            },
            'service':{
                'port':80,
                'nodeport':8080,
            }
        }
        f = open('newtree.yaml', "w")
        new = yaml.dump(tmp,f)
        f.close()
        print(new)
        return HttpResponse('ok')
    else:

        return render(request, 'cloud/format.html')