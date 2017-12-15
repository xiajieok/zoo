from cow import models
from django.db.models import Count

class AssetDashboard(object):
    def __int__(self,request):
        self.request = request
        self.asset_list = models.Asset.objects.all()
        self.data = {}
    def searilize_page(self):
        self.data['asset_categories'] = self.get_asset_categorys()
    pass