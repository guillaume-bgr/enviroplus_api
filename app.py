from flask import Flask, request
from markupsafe import escape
from services.stream_manager import StreamManager
import json

sm = StreamManager()
app = Flask(__name__)

# [(b'1673881307080-0', {b'temperature': b'10.901953820061768', b'pressure': b'735.7200047240493', b'humidity': b'27.163739922634235', b'light': b'201.1218', b'oxidised': b'74.64687168610818', b'reduced': b'1.1064372211599747', b'nh3': b'1.6745274738135645'})]
@app.route('/')
def db_persist():
    stream = sm.get_stream('rasp_output', '-', '+', 10)
    new_stream = []
    # for each tuples in stream
    for stream_tuple in stream:
        # item = list(stream_tuple)
        item_datetime = bytes.decode(stream_tuple[0])
        item_dict = {}
        for k, v in stream_tuple[1].items():
            item_dict[k.decode()] = v.decode()
        new_stream.append((item_datetime, item_dict))
    jsonStream = json.dumps(new_stream)
    return jsonStream
if __name__ == '__main__':
    app.run(port=5002)