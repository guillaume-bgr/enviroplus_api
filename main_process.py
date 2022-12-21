import controllers.all_in_one as aio
from services.stream_manager import StreamManager
import time

# Initialisation stream
stream = StreamManager()

def get_sensor_data():
    print("Adding data to the stream..")
    data = aio.get_stream_data()
    stream.append_stream('rasp_output', data)
    stream.get_stream('rasp_output', '-', '+', 1)
    # Get sensor data
    # stream.trim_stream('rasp_output', 0.2)
    

while True:
    get_sensor_data()
    time.sleep(180)
