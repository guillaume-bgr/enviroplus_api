from temperature_humidity import TemperatureHumidity
from gas import Gas
from particules import Particules
from light import Light
from noise import NoiseClass

class Main():
     def __init__(self):
        self.dict = {}
        
     def mainLoop(self):
        print("Starting collecting datas")
        self.gas = Gas()
        self.temperature_humidity = TemperatureHumidity()
        self.particules = Particules()
        self.light = Light()
        self.noise = NoiseClass()
        temperature = self.temperature_humidity.mainTemperature()
        pressure, humidity = self.temperature_humidity.getPressureHumidity()
        reds, oxis, nh3s = self.gas.read_gas_in_ppm()
        particule25, particule10, particule1 = self.particules.mainParticules()
        light, prox = self.light.mainLight()
        #noise = self.noise.mainNoise()
        datas = dict(temperature = round(temperature,2), pressure = round(pressure,2), humidity = round(humidity,2), light = round(light,2), oxidised = round(oxis,2), reduced = round(reds,2), nh3 = round(nh3s,2), particule10 = round(particule10,2), particule1 = round(particule1,2), particule25 = round(particule25,2))
        print (" Collected datas " + str(datas))
        return datas
main = Main()
main.mainLoop()      