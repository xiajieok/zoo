import requests,os

with open('sss.txt','r') as f:
    for i in f.readlines():
        i = 'http://' + i.strip()
        res = requests.get(i,)
        print(res.status_code)