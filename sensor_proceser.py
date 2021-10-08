import logging
from queue import Queue
from math import log

HUMIDITY_KEY = 0xA4
TEMPERATURE_KEY = 0xA6

def worker(input_queue: Queue, output_queue: Queue):
    while True:    
        payload: dict = input_queue.get()

        humedad = int(payload.get(HUMIDITY_KEY))
        temperatura = int(payload.get(TEMPERATURE_KEY))
        punto_de_rocio = calcularPuntoRocio(temperatura,humedad)

        print("Humedad: {}, Temperatura: {}, Punto de rocio: {}".format(humedad, temperatura,punto_de_rocio))
        
        output_entry = {'Humedad': humedad, 'Temperatura': temperatura, 'Punto de rocio': round(punto_de_rocio,3)}
        output_queue.put(output_entry)

def calcularPuntoRocio(t: int, h: int) -> float:
    a=17.7
    b=237.7
    h/=100
    punto_rocio = (b*(((a*t)/(b+t))+log(h))/(a-(((a*t)/(b+t))+log(h))))
    return punto_rocio