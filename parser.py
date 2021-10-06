import logging
from time import sleep
from queue import Queue
from protocol.package.package import Package

HUMIDITY_KEY = 0xA4
TEMPERATURE_KEY = 0xA6

RED_LED_KEY = 0xB4
GREEN_LED_KEY = 0xB5
BLUE_LED_KEY = 0xB6


def worker(input_queue: Queue, ouput_queue: Queue):
    while True:
        payload = input_queue.get()
        pack = Package(payload=payload)
        logging.info(f"Package added to Queue {pack.dict()}")
        ouput_queue.put(pack.dict())
