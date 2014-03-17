"""
Library for querying the range webservice
wangjian create it using same namespace seco.range
"""

import httplib
import json
import sys
import traceback

__version__ = '0.1'

class RangeException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Range(object):
    def __init__(self, host, user_agent=None):
        self.host = host
        self.headers = {}

    def expand(self, expr, ret_list=True):
        if isinstance(expr, list):
                expr = ','.join(expr)

        if ret_list:
            url = "/restful/tags_range/saltid?range=%s" % ( expr )
        else:
            url = "/restful/tags_range/saltid?range=%s&string=1" % ( expr )
       
        cmdb = None
        try:
            cmdb = httplib.HTTPConnection( self.host )
            cmdb.request( 'GET', url )

            res = cmdb.getresponse()

            code = res.status
            if code != 200:
                raise RangeException("Got %d response code from %s" % (code, url))
            exception = res.getheader('RangeException')
            if exception:
                raise RangeException(exception)

            if ret_list:
                jstring = res.read()
                expansion = json.loads( jstring )
                if not isinstance(expansion, list):
                    raise RangeException("Invaild Reponse Type from %s" % (url))
                expansion.sort()
                return expansion
            else:
                return res.read()
        except Exception, e:
            traceback.print_exc()
            raise RangeException(e)
        finally:
            if cmdb:
                cmdb.close()

if __name__ == '__main__':
    try:
        r = Range("localhost:3000")
    except RangeException as e:
        print e
        sys.exit(1)
    print r.expand(sys.argv[1])
