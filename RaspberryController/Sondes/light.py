import time
import logging
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

class Light():
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')

    def mainLight(self):
        lights=[]
        proxs=[]
        sumOfListLights=0
        sumOfListRange=0
        for i in range(0,6):
            lux = ltr559.get_lux()
            prox = ltr559.get_proximity()
            time.sleep(1.0)
            if i > 1:
                    lights.append(lux)
                    proxs.append(prox)
            if i == 5:
                for i in range(len(lights)):
                    sumOfListLights += lights[i]
                    averageLights = sumOfListLights/len(lights)
                for i in range(len(lights)):
                    sumOfListRange += proxs[i]
                    averageProxs = sumOfListRange/len(proxs)
                return averageLights, averageProxs