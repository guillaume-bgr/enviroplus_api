import all_in_one as aio
import stream_manager as sm

streamManager = StreamManager()
streamManager.getStream('rasp_output', '-', '+', 10)
# streamManager.appendStream('rasp_output', {'salut': 0.12, 'co': 0.25})
