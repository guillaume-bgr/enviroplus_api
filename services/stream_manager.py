from typing import Union
import redis
from datetime import datetime, timedelta
r = redis.Redis(host='localhost', port=6379, db=2)

class StreamManager :

    def append_stream(self, name: str, fields: float) :
        print(r.xadd(name, fields))

    def get_stream(self, stream_name: str, start: Union['string', 'int'], end: Union['string', 'int'], count: int) :
        print(r.xrevrange(stream_name, end, start, count))

    def trim_stream(self, stream_name: str, trim_before: float) :
        now = datetime.now()
        trim_before -= 1
        trim = now - timedelta(hours=trim_before)
        timestamp = int(trim.timestamp() * 1000)
        print(timestamp)
        print(r.xtrim(stream_name, minid=timestamp))
# streamManager = StreamManager()
# # streamManager.appendStream('rasp_output', {'salut': 0.12, 'co': 0.25})
# streamManager.getStream('rasp_output', '-', '+', 10)


