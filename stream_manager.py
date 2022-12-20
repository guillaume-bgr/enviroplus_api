from typing import Union
import redis
r = redis.Redis()
print()

class StreamManager :

    def appendStream(self, name: str, fields: float) :
        print(r.xadd(name, fields))
        
    def getStream(self, stream_name: str, start: Union['string', 'int'], end: Union['string', 'int'], count: int) :
        print(r.xrevrange(stream_name, start, end, count))
    
streamManager = StreamManager()
# streamManager.appendStream('rasp_output', {'salut': 0.12, 'co': 0.25})
streamManager.getStream('rasp_output', '-', '+', 10)


