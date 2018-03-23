from django.conf.urls import url, include
from django.contrib import admin
from cow import views

urlpatterns = [
    # url(r'^', views.index),
    # url(r'report/$', views.asset_report, name='asset_report'),
    # url(r'report/bulk_create/$',views.bulk_create_assets,name='bulk_create_assets' ),
    # url(r'^new_asset/$', views.asset_with_no_asset_id, name="new_asset"),
    # url(r'^new_assets/approval/$', views.new_assets_approval, name="new_assets_approval"),
    url(r'^nodes/', views.cloud_node, name="node"),
    url(r'^format/', views.cloud_format, name="format"),
    url(r'^management/', views.cloud_management, name="management"),



    # url(r'^asset_list/(\d+)/$', views.asset_detail, name="asset_list"),
    # url(r'^asset_list/category/$', views.asset_category, name="asset_category"),
]

