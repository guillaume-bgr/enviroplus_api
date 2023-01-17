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

    def get_avg_stream_readings(self, redis_stream: list):
        # Create a dict for data to be stored and sorted in
        data_dict = {}
        for keys in redis_stream[0][1]:
            data_dict[bytes.decode(keys)] = []
        for i in range(len(redis_stream)):
            for key in data_dict.keys(): 
                data_dict[key].append(float(bytes.decode(redis_stream[i][1][key.encode('utf-8')])))
        for data in data_dict:
            data_dict[data] = sum(data_dict[data]) / len(data_dict[data])
        return data_dict


