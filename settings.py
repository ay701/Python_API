
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'Woven'

schema_traffic = {
    # Schema definition, based on Cerberus grammar. 
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'request_log_id': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 250,
        'unique': True,
    },
    'timestamp': {
        'type': 'int',
        'minlength': 1,
        'maxlength': 15,
        'required': True,
    },
    'gae_project_name': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 250,
        'unique': True,
    },
    'gae_instance_id': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 250,
        'unique': True,
    },
    'gae_version_id': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 30,
        'unique': True,
    },
    'status': {
        'type': 'int',
        'minlength': 1,
        'maxlength': 6,
        'required': True,
    },
    'remote_ip': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 30,
        'required': True,
    },
    'version_tag': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 10,
        'unique': True,
    },

    # An embedded 'strongly-typed' dictionary.
    'json_block': {
        'type': 'dict',
        'schema': {
            'currentutc': {'type': 'string'},
            'urlparams': {'type': 'string'},
            'ctime': {'type': 'string'},
            'url': {'type': 'string'},
            'pageref': {'type': 'string'},
            'ctz': {'type': 'int'},
            'lifetime_page_views': {'type': 'int'},
            'lifetime_sessions': {'type': 'int'},
            'firstutc': {'type': 'string'},
            'lastutc': {'type': 'string'},
            'pageid': {'type': 'string'},
            'session_page_views': {'type': 'int'},
            'ua': {'type': 'string'},
            '_thredb': {'type': 'string'},
            'usersha': {'type': 'string'},
            'qlabels': {'type': 'string'},
        },
    },
}

schema_website_lastday_views = {
    'viewdate': {
        'type': 'int',
        'minlength': 1,
        'maxlength': 3,
        'required': True,
    },
    'websites': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'website': {'type': 'string'},
                'views': {'type': 'int'},
            },
        },
    },
}

schema_website_weekday_views = {
    'website': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 100,
        'unique': True,
    },
    'days': {
        'type': 'list', 
        'schema': { 
            'day': {'type': 'list', 'allowed':[1,2,3,4,5,6,7]},
            'views': {'type': 'int'} 
        },
    },
}

schema_popular_pages = {
    'date': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 10,
        'required': True,
    },
    'pages': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'rank': {'type': 'int'},
                'views': {'type': 'int'},
                'page': {'type': 'string'},
            },
        },
    },
}

schema_popular_refs = {
    'page': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 1000,
        'required': True,
    },
    'refs': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'rank': {'type': 'int'},
                'views': {'type': 'int'},
                'ref': {'type': 'string'},
            },
        },
    },
}

schema_multivisit_users = {
    'count': {
        'type': 'int',
        'minlength': 1,
        'maxlength': 10,
        'required': True,
    },
    'users': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'usersha': {'type': 'string'},
                'views': {'type': 'int'},
                'pages': {'type': 'list'}
            },
        },
    },
}

traffic = {
    # 'title' tag used in item links
    'item_title': 'traffic',

    # by default the standard item entry point is defined as
    # '/traffic/<request_log_id>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/traffic/<request_log_id>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'request_log_id'
    },

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema': schema_traffic
}

lastday_traffic = {
    'item_title': 'lastdaystraffic',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'day'
    },
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST'],
    'schema': schema_website_lastday_views
}

weekday_traffic = {
    'item_title': 'weekdaytraffic',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'website'
    },
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST'],
    'schema': schema_website_weekday_views
}

popular_pages = {
    'item_title': 'popularpages',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'date'
    },
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST'],
    'schema': schema_popular_pages
}

popular_refs = {
    'item_title': 'popularrefs',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'page'
    },      
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST'],
    'schema': schema_popular_refs
}

multivisit_users = {
    'item_title': 'multivisitusers',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'count'
    },     
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST'],
    'schema': schema_multivisit_users
}

DOMAIN = {
    'traffic': traffic, 
    'lastdaytraffic': lastday_traffic,
    'weekdaytraffic': weekday_traffic,
    'popularpages': popular_pages, 
    'popularrefs': popular_refs, 
    'multivisitusers': multivisit_users,
}
