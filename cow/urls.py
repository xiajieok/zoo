"""zoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from cow import views

urlpatterns = [
    # url(r'^', views.index),
    # url(r'report/$', views.asset_report, name='asset_report'),
    # url(r'report/bulk_create/$',views.bulk_create_assets,name='bulk_create_assets' ),
    url(r'^new_asset/$', views.asset_with_no_asset_id, name="new_asset"),
    url(r'^new_assets/approval/$', views.new_assets_approval, name="new_assets_approval"),
    url(r'^category/(.+)?/$', views.asset_category, name="category"),
    url(r'^list/(\d+)/$', views.asset_detail, name="detail"),

    # url(r'^asset_list/(\d+)/$', views.asset_detail, name="asset_list"),
    # url(r'^asset_list/category/$', views.asset_category, name="asset_category"),
]







# urlpatterns = [
#     # url(r'^', views.index),
#     url(r'^asset_list/$', views.asset_list, name="asset_list"),
#     url(r'^asset_list/(\d+)/$', views.asset_detail, name="asset_list"),
#     url(r'^asset_list/category/$', views.asset_category, name="asset_category"),
# ]
