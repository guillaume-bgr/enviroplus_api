#!/usr/bin/env python3

import time
from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

import logging

class TemperatureHumidity():
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')
        self.bus = SMBus(1)
        self.bme280 = BME280(i2c_dev=self.bus)


    # Get the temperature of the CPU for compensation
    def get_cpu_temperature(self):
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
            temp = int(temp) / 1000.0
        return temp


    def getPressureHumidity(self):
        pressures=[]
        humidities=[]
        sumOfListPressures=0
        sumOfListHumidity=0
        for i in range(0,6):
            pressure = self.bme280.get_pressure()
            humidity = self.bme280.get_humidity()
        if i > 1:
                pressures.append(pressure)
                humidities.append(humidity)
        if i == 5:
            for i in range(len(pressures)):
                sumOfListPressures += pressures[i]
            averagePressure = sumOfListPressures/len(pressures)
        
            for i in range(len(humidities)):
                sumOfListHumidity += humidities[i]
            averageHumidity = sumOfListHumidity/len(humidities)
            return averagePressure, averageHumidity
        

    def mainTemperature(self):
        temperatures=[]
        factor = 2.25
        sumOfList = 0
        for i in range(0,6):
            cpu_temps = [self.get_cpu_temperature()] * 5
            cpu_temp = self.get_cpu_temperature()
            # Smooth out with some averaging to decrease jitter
            cpu_temps = cpu_temps[1:] + [cpu_temp]
            avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
            raw_temp = self.bme280.get_temperature()
            comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
            time.sleep(1)
            if i > 1:
                temperatures.append(comp_temp)
            if i == 5:
                for i in range(len(temperatures)):
                    sumOfList += temperatures[i]
                average = sumOfList/len(temperatures)
                return average