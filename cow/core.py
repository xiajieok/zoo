import json
from cow import models
from django.core.exceptions import ObjectDoesNotExist


class Asset(object):
    def __init__(self, request):
        self.request = request
        self.mandatory_fields = ['sn', 'asset_id', 'asset_type']  # must contains 'sn' , 'asset_id' and 'asset_type'
        self.field_sets = {
            'asset': ['manufactory'],
            'server': ['model', 'cpu_count', 'cpu_core_count', 'cpu_model', 'raid_type', 'os_type', 'os_distribution',
                       'os_release'],
            'networkdevice': []
        }
        self.response = {
            'error': [],
            'info': [],
            'warning': []
        }

    def response_msg(self, msg_type, key, msg):
        if msg_type in self.response:
            self.response[msg_type].append({key: msg})
        else:
            raise ValueError

    def mandatory_check(self, data, only_check_sn=False):
        for field in self.mandatory_fields:
            if field not in data:
                self.response_msg('error', 'MandatoryCheckFailed',
                                  "The field [%s] is mandatory and not provided in your reporting data" % field)
        else:
            if self.response['error']: return False
        try:

            if not only_check_sn:
                self.asset_obj = models.Asset.objects.get(id=int(data['asset_id']), sn=data['sn'])
            else:
                self.asset_obj = models.Asset.objects.get(sn=data['sn'])
            return True
        except ObjectDoesNotExist as e:
            self.response_msg('error', 'AssetDataInvalid',
                              "Cannot find asset object in DB by using asset id [%s] and SN [%s] " % (
                                  data['asset_id'], data['sn']))
            self.waiting_approval = True
            return False

    def data_is_valid_without_id(self):
        '''when there's no asset id in reporting data ,goes through this function fisrt'''

        data = self.request.POST.get("asset_data")
        print(data)
        if data:
            try:
                data = json.loads(data)
                asset_obj = models.Asset.objects.get_or_create(sn=data.get('sn'), name=data.get(
                        'sn'))  # push asset id into reporting data before doing the mandatory check
                data['asset_id'] = asset_obj[0].id
                self.mandatory_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError as e:
                self.response_msg('error', 'AssetDataInvalid', str(e))
        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")

    def get_asset_id_by_sn(self):
        '''
        When the client first time reports it's data to Server,
        it doesn't know it's asset id yet,so it will come to the server asks for the asset it first,
        then report the data again
        '''
        data = self.request.POST.get("asset_data")
        print('获取的数据',data)
        response = {}
        if data:
            try:
                data = json.loads(data)
                if self.mandatory_check(data,only_check_sn=True):  # the asset is already exist in DB,just return it's asset id to client
                    response = {'asset_id': self.asset_obj.id}
                else:
                    if hasattr(self, 'waiting_approval'):
                        response = {
                            'needs_aproval': "this is a new asset,needs IT admin's approval to create the new asset id."}
                        self.clean_data = data
                        self.save_new_asset_to_approval_zone()
                        print(response)
                    else:
                        response = self.response
            except ValueError as e:
                self.response_msg('error', 'AssetDataInvalid', str(e))
                response = self.response
        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")
            response = self.response
        print('获取的新的或者旧的ID',response)
        return response

    def save_new_asset_to_approval_zone(self):
        '''When find out it is a new asset, will save the data into approval zone to waiting for IT admin's approvals'''
        asset_sn = self.clean_data.get('sn')
        asset_already_in_approval_zone = models.NewAssetApprovalZone.objects.get_or_create(sn=asset_sn,
                                                                                           data=json.dumps(
                                                                                                   self.clean_data),
                                                                                           manufactory=self.clean_data.get(
                                                                                                   'manufactory'),
                                                                                           model=self.clean_data.get(
                                                                                                   'model'),
                                                                                           asset_type=self.clean_data.get(
                                                                                                   'asset_type'),
                                                                                           ram_size=self.clean_data.get(
                                                                                                   'ram_size'),
                                                                                           cpu_model=self.clean_data.get(
                                                                                                   'cpu_model'),
                                                                                           cpu_count=self.clean_data.get(
                                                                                                   'cpu_count'),
                                                                                           cpu_core_count=self.clean_data.get(
                                                                                                   'cpu_core_count'),
                                                                                           os_distribution=self.clean_data.get(
                                                                                                   'os_distribution'),
                                                                                           os_release=self.clean_data.get(
                                                                                                   'os_release'),
                                                                                           os_type=self.clean_data.get(
                                                                                                   'os_type'),

                                                                                           )
        return True
    def data_is_valid(self):
        data = self.request.POST.get("asset_data")
        if data:
            try:
                data = json.loads(data)
                self.mandatory_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError as e:
                self.response_msg('error', 'AssetDataInvalid', str(e))
        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")
