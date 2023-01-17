# from services.stream_manager import StreamManager

# # Initialisation stream
# stream = StreamManager()

# def avg_sensor_data():
#     stream_data = stream.get_stream('rasp_output', '-', '+', 100)
#     cat_data = []
#     cat_temp = []
#     for i in range(0, len(stream_data)):
#         datadict = list(stream_data[i][1].values())
#         for y in range(0, len(datadict)):
#             cat_temp.append(datadict[y])
#         cat_data.append(cat_temp)
#     print(cat_data)
#         # value_list = list(data[1].values())
#         # stream_data[i]
#     #     for value in value_list :

# # Get sensor data
# # stream.trim_stream('rasp_output', 0.2)
    
# avg_sensor_data()
# # while True:
# #     get_sensor_data()
# #     time.sleep(180)
