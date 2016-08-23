from flask import Flask
from flask import render_template
from flask.ext.pymongo import PyMongo
from datetime import datetime, timedelta
from pprint import pprint
from flask import request
import requests_cache

app = Flask(__name__)
requests_cache.install_cache('github_cache', None, expire_after=180)

app.name = "Woven"
mongo = PyMongo(app)

@app.route('/')
def index():
    return 'Welcome to Woven Traffic Application'

@app.route('/pastdaystraffic/<int:days>')
def pastdays_traffic(days):

    # Get date before n days 
    #startDate = datetime.now() - timedelta(days=days)
    startDate = "2016-06-06"
    pastviews = mongo.db.websitestats.aggregate([
                                                    {"$match":{"viewdate":{"$gte":startDate}}},
                                                    {"$group":{"_id":"$website", "totalviews":{"$sum":"$views"}}}, 
                                                    {"$sort":{"totalviews":-1}}
                                                ]
                                                )
    return render_template('pastviews.html', day=days, pastviews=pastviews)

@app.route('/weekdaystraffic/<website>')
def show_week_days_traffic(website):
  
    # Get week start, end date
    #dt = datetime.strptime('06062016', "%d%m%Y").date()
    dt = datetime.now()
    week_start = dt- timedelta(days=dt.weekday())
    week_end = week_start + timedelta(days=6)
    weekviews = mongo.db.websitestats.aggregate([
                                                    {"$match":{"website":website,"viewdate":{"$gte":week_start},"viewdate":{"$lte":week_end}}},
                                                    {"$group":{"_id":"$viewdate", "totalviews":{"$sum":"$views"}}}, 
                                                    {"$sort":{"totalviews":-1}}
                                                ]
                                                )
    return render_template('weekviews.html', website=website, weekviews=weekviews)

@app.route('/popularpages/<date>/<int:num>')
def show_popular_pages(date,num):
    popularpages = mongo.db.pagestats.aggregate([
                                                    {"$match":{"viewdate":date}},
                                                    {"$group":{"_id":"$page", "totalviews":{"$sum":"$views"}}}, 
                                                    {"$sort":{"totalviews":-1}},
                                                    {"$limit":num}
                                                ]
                                                )
    return render_template('popularpages.html', date=date, num=num, popularpages=popularpages)

@app.route('/popularrefs/<pageid>/<int:num>')
def show_popular_refs(pageid,num):
    #popularrefs = mongo.db.traffic.find_one()
    refs = mongo.db.refstats.aggregate([
                                                    {"$match":{"pageid":pageid}},
                                                    {"$group":{"_id":"$ref", "total_ref_cnt":{"$sum":"$ref_cnt"}}}, 
                                                    {"$sort":{"total_ref_cnt":-1}},
                                                    {"$limit":num}
                                                ]
                                                )
    #pprint (vars(refs))
    return render_template('popularrefs.html', pageid=pageid, num=num, refs=refs)

@app.route('/multiviews')
def show_multi_visit_users():
    #multiviews = mongo.db.traffic.find_one()
    users = mongo.db.userwebsitestats.aggregate([
                                                    {"$group":{ "_id":{"user":"$user", "website":"$website"}, 
                                                                "total_cnt":{"$sum":"$cnt"},
                                                                "$addToSet":{"allpages":"$pages"}
                                                                }
                                                    }, 
                                                    {"$sort":{"total_cnt":-1}},
                                                    {"$match":{"total_cnt":{"$gt":1}}},
                                                    {"$limit":1}
                                                ]
                                                )
    return render_template('multiviews.html', users=users)
    #return 'Last %s day' % day

@app.route('/postjson', methods=['GET','POST'])
def postjson():
    # fake json data
    jsons = [{ "status" : "200", "b64_length" : "536", "json_block" : { "currentutc" : "1465173233329", "urlparams" : "", "ctime" : "1465173233324", "url" : "http://uproxx.com/filmdrunk/weekend-box-office-tmnt/", "pageref" : "", "ctz" : 300, "lifetime_page_views" : 1, "lifetime_sessions" : 1, "firstutc" : "1465173233329", "lastutc" : "1465173233329", "inst_article" : 1, "pageid" : "", "session_page_views" : 1, "ua" : "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920P Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/50.0.2661.86 Mobile Safari/537.36 [FBIA/FB4A;FBAV/79.0.0.18.71;]", "_thredb" : "uproxx.06a4923fc5cb43719ab90f310768dfa0.1465173233329.1465173233329.1465173233329.1.1", "usersha" : "06a4923fc5cb43719ab90f310768dfa0", "qlabels" : "" }, "request_log_id" : "6754c4f200ff06e9a1b87fec300001737e737465616d2d686f7573652d3932383135000132303136303431342d6d617374657200010104", "timestamp" : "1465173234457", "gae_project_name" : "steam-house-92815", "version_tag" : "v2", "gae_version_id" : "20160414-master", "gae_instance_id" : "00c61b117c99515979d47cadaca5a47f97cffb00666fb4d11550fab82e59230ecd", "remote_ip" : "173.174.153.101" },
{ "status" : "200", "b64_length" : "484", "json_block" : { "currentutc" : "1465173414791", "urlparams" : "", "ctime" : "1465173414791", "url" : "http://brobible.com/girls/article/jessica-simpson-swimsuit-pics/", "pageref" : "http://brobible.com/girls/page/3/", "ctz" : 420, "lifetime_page_views" : 69, "lifetime_sessions" : 1, "firstutc" : "1465170054105", "lastutc" : "1465173360217", "pageid" : 22537829, "session_page_views" : 1, "ua" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17", "_thredb" : "brobible.4ba20eff762b4b90bae760a93ae9450f.1465170054105.1465173360217.1465173414791.69.1", "usersha" : "4ba20eff762b4b90bae760a93ae9450f", "qlabels" : "" }, "request_log_id" : "7754c5a600ff0d59b02d33c7920001737e737465616d2d686f7573652d3932383135000132303136303431342d6d617374657200010104", "timestamp" : "1465173414877", "gae_project_name" : "steam-house-92815", "version_tag" : "v2", "gae_version_id" : "20160414-master", "gae_instance_id" : "00c61b117c254f4c3183d0f589d83f283b022df2c1eac23c0bed529d237d9938", "remote_ip" : "2600:8801:7f03:a00:4150:259:6154:18d3" }]
    result = mongo.db.traffic.insert(jsons)
    return "Success"

@app.route('/hello')
def hello_world():
    pastviews = mongo.db.traffic.find_one()
    return render_template('pastviews.html', pastviews=pastviews)

if __name__ == '__main__':
    app.run()
