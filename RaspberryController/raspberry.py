import time

from RaspberryController.Sondes.temperature_humidity import TemperatureHumidity
from RaspberryController.Sondes.gas import Gas
from RaspberryController.Sondes.particules import Particules
from RaspberryController.Sondes.light import Light
from RaspberryController.Sondes.noise import NoiseClass
from RaspberryController.Display.display import LCD

class Raspberry():
   def __init__(self):
      self.gas = Gas()
      self.temperature_humidity = TemperatureHumidity()
      self.particules = Particules()
      self.light = Light()
      self.noise = NoiseClass()
      self.lcd = LCD()
      
   def displayData(self, text, fontSize=15, backgroudColor = (255,255,255), fontColor = (0,0,0), displayTime = 10):
            if text:
               self.lcd.displayText(fontSize,fontColor, backgroudColor, text)
            else:
               self.lcd.displayText(fontSize,fontColor, (255,0,0), 'Ereur Aucune donnée à afficher')  
            time.sleep(displayTime)
            self.lcd.stopLCD()
   def constructTextData(self, datas):
            if datas is not None:
                     text ="""Température: {:05.2f} *C
                     Pression: {:05.2f} hPa
                     Humiditée: {:05.2f} %
                     Lumière: {:05.2f} lux
                     Gas: Oxydants: {:05.2f} ppm, Réducteurs : {:05.2f} ppm, Nh3: {:05.2f} ppm, 
                     Particule: Pm 10 : {:05.2f} ug/m3, Pm 2,5 : {:05.2f} ug/m3, Pm 1 : {:05.2f} ug/m3
                     """.format(datas['temperature'], datas['pressure'], datas['humidity'], datas['light'], datas['oxidised'], datas['reduced'], datas['nh3'], datas['particule10'], datas['particule25'],datas['particule1'] )
                     return text
   def mainLoop(self):
      print("Starting collecting datas")
      temperature = self.temperature_humidity.mainTemperature()
      pressure, humidity = self.temperature_humidity.getPressureHumidity()
      reds, oxis, nh3s = self.gas.read_gas_in_ppm()
      particule25, particule10, particule1 = self.particules.mainParticules()
      light, prox = self.light.mainLight()
      #noise = self.noise.mainNoise()
      datas = dict(temperature = round(temperature,2), pressure = round(pressure,2), humidity = round(humidity,2), light = round(light,2), oxidised = round(oxis,2), reduced = round(reds,2), nh3 = round(nh3s,2), particule10 = round(particule10,2), particule1 = round(particule1,2), particule25 = round(particule25,2))
      print (" Collected datas " + str(datas))
      text = self.constructTextData(datas)
      self.displayData(text)
      return datas


      