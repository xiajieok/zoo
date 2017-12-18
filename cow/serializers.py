#_*_coding:utf-8_*_
# from assets.myauth import UserProfile
from cow import models
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ('url', 'name', 'email')


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        depth=2
        fields = ('name', 'sn','server','networkdevice','securitydevice','storagedevice')


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server
        #fields = ('name', 'sn','server')