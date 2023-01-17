from flask import Flask, request
from markupsafe import escape
from services.stream_manager import StreamManager
import json

sm = StreamManager()
app = Flask(__name__)

@app.route('/')
def db_persist():
    stream = sm.get_stream('rasp_output', '-', '+', 10)
    new_stream = []
    for stream_tuple in stream:
        item_datetime = bytes.decode(stream_tuple[0])
        item_dict = {}
        for k, v in stream_tuple[1].items():
            item_dict[k.decode()] = v.decode()
        new_stream.append((item_datetime, item_dict))
    jsonStream = json.dumps(new_stream)
    return jsonStream
if __name__ == '__main__':
    app.run(port=5002)