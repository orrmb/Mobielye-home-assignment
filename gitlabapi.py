import json
import gitlab

repo = 'orb-home-assignment/orb-test'
username = 'orcom2000'


gl = gitlab.Gitlab(url='https://gitlab.com', private_token=TOKEN)
try:
    mrs = group.mergerequests.list()
except:
    print('Error')

