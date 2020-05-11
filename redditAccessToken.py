import requests

import os   
      
# Get the current working   
# directory (CWD)   
cwd = os.getcwd()  
print(cwd)

base_url = 'https://oauth.reddit.com'

f = open("accessToken.txt", "r")
token = f.read()
f.close()

headers = {'Authorization': token, 'User-Agent': 'APP-NAME by REDDIT-USERNAME'}
response = requests.get(base_url + '/api/v1/me', headers=headers)

if response.status_code == 200:
    print(response.json()['name'], response.json()['comment_karma'])
else:
    info = {}
    with open("info.txt") as f:
        for line in f:
            (key, val) = line.split()
            info[key] = val
    f.close()

    base_url = 'https://www.reddit.com/'
    data = {'grant_type': 'password', 'username': info["username"], 'password': info["password"]}

    OAuthSecret = info["secret"]
    

    auth = requests.auth.HTTPBasicAuth("tg7emkHIi5Ggow", info["secret"])
    r = requests.post(base_url + 'api/v1/access_token',
                    data=data,
                    headers={'user-agent': 'APP-NAME by REDDIT-USERNAME'},
            auth=auth)
    d = r.json()

    token = d['access_token']

    f = open("accessToken.txt", "w")
    f.write('bearer ' + d['access_token'])
    f.close()