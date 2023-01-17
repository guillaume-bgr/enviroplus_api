import time
from pms5003 import PMS5003, ReadTimeoutError
import logging
class Particules:
    
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')
        self.pms5003 = PMS5003()
        time.sleep(1.0)
    def mainParticules(self):
        print ("Start Collecting Particules datas")
        if self.pms5003:
             sumOfList1 = 0
             sumOfList2 = 0
             sumOfList3 = 0
             particules1=[]
             particules2=[]
             particules3=[]
            
             for i in range(0,6):
                try:
                    readings = self.pms5003.read()
                    part1 = readings.pm_ug_per_m3(2.5)
                    part2 = readings.pm_ug_per_m3(10)
                    part3 = readings.pm_ug_per_m3(1.0)
                    time.sleep(1.0)
                    if i > 1:
                         particules1.append(part1)
                         particules2.append(part2)
                         particules3.append(part3)
                    if i == 5:
                        for i in range(len(particules1)):
                            sumOfList1 += particules1[i]
                        average1 = sumOfList1/len(particules1)
                        for i in range(len(particules2)):
                            sumOfList2 += particules2[i]
                        average2 = sumOfList2/len(particules2)
                        for i in range(len(particules3)):
                            sumOfList3 += particules3[i]
                        average3 = sumOfList3/len(particules3)
                        print ("End Collecting Particules datas")
                        return average1, average2, average3
                except ReadTimeoutError:
                    self.mainParticules()
                    