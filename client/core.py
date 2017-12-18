# import os, sys, platform, subprocess
#
# system = platform.system()
#
#
# class Linux(object):
#     filter_keys = ['Manufacturer', 'Serial Number', 'Product Name', 'UUID', 'Wake-up Type']
#     raw_data = {}
#     for key in filter_keys:
#         cmd = 'dmidecode  -t system |grep "%s"' % key
#         # print(cmd)
#         res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#         msg = res.stdout.read()
#         msg = str(msg, encoding='utf-8').strip().split(':')
#         raw_data[key] = msg[1].strip()
#         print(raw_data)
#     data = {"asset_type": 'server'}
#     data['manufactory'] = raw_data['Manufacturer']
#     data['sn'] = raw_data['Serial Number']
#     data['model'] = raw_data['Product Name']
#     data['uuid'] = raw_data['UUID']
#     data['wake_up_type'] = raw_data['Wake-up Type']
#
#     def raminfo(self):
#         pass
#
#
# class Windwos(object):
#     print('This is Windows')
#
#
# if __name__ == '__main__':
#
#     if system == 'Linux':
#         Linux()
#     else:
#         Windwos()
#         print('hahha')
