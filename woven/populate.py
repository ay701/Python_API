import json
import time
import datetime
from datetime import date
from urlparse import urlparse
from pymongo import MongoClient

client = MongoClient()
db = client.Woven

i = datetime.datetime.now()

with open('beacon_sample_data.json', 'r') as f:
    contents = f.read()

json_data = [json.loads(str(item)) for item in contents.strip().split('\n')]

for e in json_data:
    for k, v in e.items():
        if k == 'remote_ip':
            user = v

        if k == 'json_block':
            e[k] = json.loads(v)

            for key, val in e[k].items():
                if key == 'ctime':
                    cdate = time.strftime("%Y-%m-%d", time.gmtime(val/1000))

                if key == 'pageref':
                    ref = val

                if key == 'pageid':
                    pageid = val

                if key == 'url':
                    url = val
                    parsed_uri = urlparse( url )
                    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    db.websitestats.update({"viewdate":cdate, "website":domain}, {"$push": {"pages": url}, "$inc": {"views":1}}, upsert=True)
    db.userstats.update({"viewdate":cdate, "user":user}, {"$push": {"websites":domain, "pages": url}}, upsert=True)
    db.pagestats.update({"viewdate":cdate, "page":url}, {"$push": {"users":user}, "$inc": {"views":1}}, upsert=True)
    db.refstats.update({"pageid":pageid,"ref":ref}, {"$set": {"page":url}, "$inc": {"ref_cnt":1}}, upsert=True)
    db.userwebsitestats.update({"user":user,"website":domain}, {"$push": {"pages": url}, "$inc": {"cnt":1}}, upsert=True)
    result = db.traffic.insert_one(e)
