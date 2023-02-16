import ST7735
from PIL import Image, ImageDraw
from enviroplus.noise import Noise
import time

class NoiseClass():
    def __init__(self):
        self.noise = Noise()
    def mainNoise(self):
        sumOfList0 = 0
        sumOfList1 = 0
        sumOfList2 = 0
        lows=[]
        mids=[]
        highs=[]
        amps=[]
        print("Start collecting Noise datas")
        for i in range(0,6):
            low, mid, high, amp = self.noise.get_noise_profile()
            time.sleep(1.0)
            if i > 1:
                    low *= 128
                    mid *= 128
                    high *= 128
                    amp *= 64
                    lows.append(low)
                    mids.append(mid)
                    highs.append(high)
                    amps.append(amp)
            if i == 5:
                for i in range(len(lows)):
                    sumOfList0 += lows[i]
                    averageAmps0 = sumOfList0/len(lows)
                for i in range(len(mids)):
                    sumOfList1 += mids[i]
                    averageAmps1 = sumOfList1/len(mids)
                for i in range(len(highs)):
                    sumOfList2 += highs[i]
                    averageAmps2 = sumOfList2/len(highs)
                for i in range(len(amps)):
                    sumOfList2 += amps[i]
                    averageAmps2 = sumOfList2/len(amps)
                print("End collecting noise data")
                return averageAmps0, averageAmps1,averageAmps2

