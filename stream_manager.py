import redis
r = redis.Redis()
r.ping()
# r.xadd(name, fields, id='*', maxlen=None, approximate=True, nomkstrea m=False, minid=None, limit=None)
# class StreamManager :

# def appendStream() :
#     r.xadd(name, fields, id='*', maxlen=None, approximate=True, nomkstream=False, minid=None, limit=None)