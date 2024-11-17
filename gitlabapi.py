import json

import gitlab



gl = gitlab.Gitlab(url='https://gitlab.com', private_token=TOKEN)
try:
    projects = gl.projects.list(owned=True, search='orb-test')
    print(projects)
except:
    print('Error')