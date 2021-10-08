import logging
from queue import Queue
from json import dumps
import paho.mqtt.client as mqtt
from time import sleep

from protocol.datalink.datalink import Datalink

TOPIC_NAME_BASE = 'SDA/Equipo_DMS/'
TOPIC_COLOR_LED = TOPIC_NAME_BASE + 'LED/Color'

RED_LED_KEY = 0xB4
GREEN_LED_KEY = 0xB5
BLUE_LED_KEY = 0xB6

def on_message(client, userdata, message):
    received_message = str(message.payload.decode("utf-8"))
    received_message = received_message.lstrip("#")
    logging.info(f"Mensaje recibido: {received_message}")

    if message.topic == TOPIC_COLOR_LED: 
        # Separo el mensaje de color en cada byte 
        p1 = bytes(received_message[0:2],'ascii')
        p2 = bytes(received_message[2:4],'ascii')
        p3 = bytes(received_message[4:6],'ascii')

        # Creo un diccionario con los byte de los colores
        dic = {
            RED_LED_KEY:int(p1,16),
            GREEN_LED_KEY:int(p2,16),
            BLUE_LED_KEY:int(p3,16)
        }

        # Enviar data a traves del serial
        global link_local       
        link_local.sendData(dic)
        sleep(0.1)
        
def worker(link: Datalink):
    client = mqtt.Client(client_id="py-reciever")
    client.on_message=on_message
    client.connect(host="broker.hivemq.com", port=1883)
    client.subscribe(topic=TOPIC_COLOR_LED,qos=1)
    # se utiliza una variable global para poder usarla en la funcion on_message
    # TODO: Crear una clase propia que herede metodos de la clase Datalink y client
    # para eliminar la necesidad de variable global
    global link_local
    link_local = link

    while True:
        client.loop()
        sleep(0.1)
        