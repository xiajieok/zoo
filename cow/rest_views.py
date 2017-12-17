#_*_coding:utf-8_*_
__author__ = 'jieli'
# from cow import  myauth
from rest_framework import viewsets
# from cow.serializers import UserSerializer, cowerializer,ServerSerializer
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from cow import models
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import json

