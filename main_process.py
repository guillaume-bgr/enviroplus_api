import controllers.all_in_one as aio
from services.stream_manager import StreamManager
import time

sm = StreamManager()

def main_process():
    while True:
        sm.append_stream('rasp_output', aio.get_stream_data())
        print((sm.get_stream('rasp_output', '-', '+', 10)))
        time.sleep(180)

main_process()

