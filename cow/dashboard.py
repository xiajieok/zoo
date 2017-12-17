from cow import models
from django.db.models import Count


class AssetDashboard(object):
	'''
	统计资产信息，统计设备数量，取出子类型name
	:return  返回格式 {"asset_categories": {"data": [2, 1], "names": ["PC\u670d\u52a1\u5668", "\u8def\u7531\u5668"]}}

	'''
	def __init__(self, request):
		self.request = request
		self.asset_list = models.Asset.objects.all()
		self.data = {}

	def searilize_page(self):
		self.data['asset_categories'] = self.get_asset_categories()

	def get_asset_categories(self):
		'''按资产类型进行分类'''

		dataset = {
			'names': [],
			'data': []
		}
		# 设置一个字典，格式为{ 设备类型：数量}
		prefetch_data = {
			models.Server: None,
			models.NetworkDevice: None,
			models.SecurityDevice: None,
			models.Software: None,
		}
		for key in prefetch_data:
			'''
			循环字典的key,将资产类型聚合统计出各资产的总数，生成列表【{资产类型：总数}】
			'''
			data_list = list(key.objects.values('sub_asset_type').annotate(total=Count('sub_asset_type')))
			for index, category in enumerate(data_list):
				'''				 
				循环各类型设备的子类型，判断type是否相等，如果相等，就取出来这个子类型，塞给data_list
				'''
				for db_val, display_name in key.sub_assset_type_choices:
					if category['sub_asset_type'] == db_val:
						data_list[index]['name'] = display_name
			for item in data_list:
				'''
				循环data_list 将取到的子类型name和统计结果添加到 dataset
				注意此处 name 和 data是固定格式，不可更改
				'''
				dataset['names'].append(item['name'])
				dataset['data'].append(item['total'])
		# prefetch_data[key] = data_list
		return dataset
# print("prefecth data",prefetch_data)
# print("dataset",dataset)
