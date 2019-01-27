import json
from pprint import pprint
import requests
import re

access_token = ''

profile_id = ''

categories ='books{category,genre,name},music{artists_we_like,band_interests,genre,category,name},movies{artists_we_like,genre,category,name},education,quotes'
def get_fields(cats):
    filtered = re.sub("[\{].*?[\}]", "", cats)
    fields = filtered.split(',')
    return fields

def get_data (access_token,profile_id,data):
    info={}
    fields = get_fields(data)
    url = "https://graph.facebook.com/v3.2/{}?fields={}&access_token={}".format(profile_id,data,access_token)
    req = requests.get(url)
    r = json.loads(req.content)
    for field in fields:
        try:
            req = r[field]
        except KeyError:
            print("{} data is not accesseble,skipping".format(field))
            continue
        if 'paging' in req:
            information = req["data"]
            while 'next' in req["paging"]:
                req = json.loads(requests.get(req["paging"]["next"]).content)
                for lines in req["data"]:
                    information.append(lines)
            info[field]=information
        else:
            info[field] = r[field]
    return info

cats = get_data(access_token,profile_id,categories)
req_fields = get_fields(categories)
for field in req_fields:
    with open(field+".csv",'w') as f:
        try:
            for item in cats[field]:
                f.write("%s\n" % item)
        except KeyError:
            continue



