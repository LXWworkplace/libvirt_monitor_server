# coding: utf-8
import sys
try:
    from gevent import monkey
    monkey.patch_all()
    from gevent.wsgi import WSGIServer
    import gevent
except (ImportError,ImportWarning) as e:
    print "Can not find python-gevent, in ubuntu just run \"sudo apt-get install python-gevent\"."
    print e
    sys.exit(1)

import os
import json
import time
import mimerender
from cloud_monitor_settings import *

try:
    import web
except (ImportError,ImportWarning) as e:
    print "Can not find python-webpy, in ubuntu just run \"sudo apt-get install python-webpy\"."
    print e
    sys.exit(1)

mimerender = mimerender.WebPyMimeRender()
web.config.debug = True

db = web.database(dbn=db_engine,host=db_server,db=db_database,user=db_username,pw=db_password)

render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda **args: json.dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message

class getInstanceList(object):
    @mimerender(
        default = 'json',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
    )
    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        table = 'cloud_host'
        try:
            results = list()
            ret = db.select(table,what='id,uuid,ip,enable')
            for line in ret:
                results.append(dict(line))
        except Exception,e:
            raise web.internalerror(message=e)
        return {'message':results}

class setInterval():
    @mimerender(
        default = 'json',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
    )
    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        table='cloud_config'
        data = web.input()
        try:
            interval = data.interval
        except AttributeError:
            return {'message':'attribute_error'}
        if int(interval)<=0:
            return {'message':'failed, interval too short'}
        elif int(interval)>=3600: 
            return {'message':'failed, interval too long'}
        db.update(table,where="`key`='interval'",value=interval)
        return {'message':'success, new interval is '+interval}

class enableByUUID():
    @mimerender(
        default='json',
        html = render_html,
        xml = render_xml,
        json = render_json,
        txt = render_txt
    )
    def POST(self, uuid):
        import datetime
        table = 'cloud_host'
        data = web.input()
        try:
            enable = data.enable
        except AttributeError:
            return {'message':'attribute_error'}
        try:
            db.update(table,where="`uuid`='%s'" % uuid,enable=int(enable))
            return {'message':'success'}
        except Exception,e:
            raise web.notfound(message=e)       

class getDataByUUID():
    @mimerender(
        default='json',
        html = render_html,
        xml = render_xml,
        json = render_json,
        txt = render_txt
    )
    def POST(self, uuid):
        web.header('Access-Control-Allow-Origin','*')
        table = 'cloud_result'
        data = web.input()
        try:
            stime = data.stime
            etime = data.etime
        except AttributeError:
            return {'message':'attribute_error'}
        try:
            ret = db.select(table,where="`time`>='%s' and `time`<='%s' and `uuid`='%s'" % (stime,etime,uuid))
            results = list()
            for line in ret:
                results.append(dict(line))
        except Exception,e:
            raise web.internalerror(message=e)
        return {'message':results}

if __name__ == '__main__':

    urls = (
        # 列出所有instance
        '/instances','getInstanceList',
        # 按时间起始结束，获取指定uuid的instance数据
        '/instances/(.*)','getDataByUUID',
        # 设置抓取数据间隔（秒）
        '/interval','setInterval',
        # 设置是否抓取指定uuid的instance
        '/enable/(.*)','enableByUUID',
    )
    try:
        application = web.application(urls, globals()).wsgifunc()
        WSGIServer(('', api_server_port), application).serve_forever()

    except KeyboardInterrupt:
        pass
    
    
