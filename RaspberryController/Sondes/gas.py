
import math
import time
from enviroplus import gas

class Gas :
    def __init__(self):
        self.gas = gas
    def read_raw_gas(self):
        gas_data = self.gas.read_all()
        raw_red_rs = round(gas_data.reducing, 0)
        raw_oxi_rs = round(gas_data.oxidising, 0)
        raw_nh3_rs = round(gas_data.nh3, 0)
        return raw_red_rs, raw_oxi_rs, raw_nh3_rs
    
    def read_gas_in_ppm(self):
        # Set up startup gas sensors' R0 with no compensation (Compensation will be set up after warm up time)
        reds=[]
        oxis = []
        nh3s=[]
        sumOfListReds = 0
        sumOfListOxis = 0
        sumOfListNh3s = 0
        
        for i in range(0,6):
            raw_red_rs, raw_oxi_rs, raw_nh3_rs = self.read_raw_gas()
            comp_red_rs = raw_red_rs
            comp_oxi_rs = raw_oxi_rs
            comp_nh3_rs = raw_nh3_rs
            red_r0, oxi_r0, nh3_r0 = self.read_raw_gas()
            if comp_red_rs/red_r0 > 0:
                red_ratio = comp_red_rs/red_r0
            else:
                red_ratio = 0.0001
            if comp_oxi_rs/oxi_r0 > 0:
                oxi_ratio = comp_oxi_rs/oxi_r0
            else:
                oxi_ratio = 0.0001
            if comp_nh3_rs/nh3_r0 > 0:
                nh3_ratio = comp_nh3_rs/nh3_r0
            else:
                nh3_ratio = 0.0001
            red_in_ppm = math.pow(10, -1.25 * math.log10(red_ratio) + 0.64)
            oxi_in_ppm = math.pow(10, math.log10(oxi_ratio) - 0.8129)
            nh3_in_ppm = math.pow(10, -1.8 * math.log10(nh3_ratio) - 0.163)
            time.sleep(1)
            if i > 1:
                    reds.append(red_in_ppm)
                    oxis.append(oxi_in_ppm)
                    nh3s.append(nh3_in_ppm)
            if i == 5:
                for i in range(len(reds)):
                        sumOfListReds += reds[i]
                for i in range(len(oxis)):
                        sumOfListOxis += oxis[i]
                for i in range(len(nh3s)):
                        sumOfListNh3s += nh3s[i]
                averageReds = sumOfListReds/len(reds)
                averageOxis = sumOfListOxis/len(oxis)
                averageNh3s = sumOfListNh3s/len(nh3s)
                
                
        return averageReds,averageOxis,averageNh3s

        