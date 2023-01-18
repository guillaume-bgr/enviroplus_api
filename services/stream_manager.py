from typing import Union
import redis
from datetime import datetime, timedelta
r = redis.Redis(host='localhost', port=6379, db=2)

class StreamManager :
    def append_stream(self, name: str, fields: float) :
        return r.xadd(name, fields)

    def get_stream(self, stream_name: str, start: Union['string', 'int'], end: Union['string', 'int'], count: int) :
        return r.xrevrange(stream_name, end, start, count)

    def trim_stream(self, stream_name: str, trim_before: float) :
        now = datetime.now()
        trim_before -= 1
        trim = now - timedelta(hours=trim_before)
        timestamp = int(trim.timestamp() * 1000)
        return r.xtrim(stream_name, minid=timestamp)
