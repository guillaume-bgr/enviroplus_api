import redis
r = redis.Redis(host='localhost', port=6379, db=2)

r.get('foo')
