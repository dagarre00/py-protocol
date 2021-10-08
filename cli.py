import logging
from serial import Serial
from queue import Queue
from threading import Thread

from protocol.datalink.datalink import Datalink

import parser
import producer
import receiver
import sensor_proceser


serial_input_queue = Queue()
serial_output_queue = Queue()

parser_output_queue = Queue()
proceser_output_queue = Queue()
receiver_output_queue = Queue()

input_package =  Queue()

uart = Serial("/dev/ttyUSB0", 115200, timeout=0.1)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
logging.info("Program Running")

link = Datalink(
    header=0x7E, uart=uart, input_queue=serial_input_queue, output_queue=serial_output_queue
)

Thread(target=link.run).start()
Thread(target=parser.worker, args=(serial_input_queue, parser_output_queue)).start()
Thread(target=sensor_proceser.worker, args=(parser_output_queue,proceser_output_queue)).start()
Thread(target=producer.worker, args=(proceser_output_queue,)).start()
Thread(target=receiver.worker, args=(link,)).start()

producer.client.loop_forever()
