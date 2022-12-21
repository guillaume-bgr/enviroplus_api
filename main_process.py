import controllers.all_in_one as aio
from services.stream_manager import StreamManager
import time

# Initialisation stream
stream = StreamManager()

def main_process():
    print("Adding data to the stream..")
    # Get sensor data
    # datas = aio.get_stream_data()
    # stream.get_stream('rasp_output', '-', '+', 10)
    stream.trim_stream('rasp_output', 0.2)
    
    # stream.append_stream('rasp_output', datas)

while True:
    main_process()
    time.sleep(5)
