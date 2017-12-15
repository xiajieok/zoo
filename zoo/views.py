from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from cow import models
import cow.asset_handle as asset_handle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate


def index(request):
    return render(request,'index.html',)
