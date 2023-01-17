from RaspberryController.raspberry import Raspberry 
from services.stream_manager import StreamManager
import time

rasp = Raspberry()

sm = StreamManager()

def main_process():
    while True:
        sm.append_stream('rasp_output', rasp.mainLoop())
        print((sm.get_stream('rasp_output', '-', '+', 10)))
        time.sleep(180)

main_process()

