# -*- coding: utf-8 -*-
import logging
from time import sleep
from serial import Serial
from queue import Queue

class Datalink:
    def __init__(self, header: int, uart: Serial, input_queue: Queue, output_queue: Queue):
        self._header = header
        self._uart = uart
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._active = False

    @staticmethod
    def _calculate_checksum(payload: bytes) -> bytes:
        return (0xFF - sum([x for x in payload])%256).to_bytes(
            1, byteorder="big", signed=False
        )

    def sendData(self,payload: dict)->bytes:
        data = b''
        data += self._header.to_bytes(1,byteorder="big",signed=False) 
        local_data=b''
        for key in payload:
            local_data += key.to_bytes(1,byteorder="big",signed=False) 
            local_data += payload[key].to_bytes(2,byteorder="big",signed=False) 
        data += len(local_data).to_bytes(1,byteorder="big",signed=False) 
        data += local_data
        checksum = self._calculate_checksum(local_data)       
        data += checksum
        self._uart.write(data)
        return data


    def run(self):
        self._active = True
        while self._active:
            header = int.from_bytes(self._uart.read(), byteorder="big", signed=False)
            if header == self._header:
                lenght = int.from_bytes(
                    self._uart.read(), byteorder="big", signed=False
                )
                payload = self._uart.read(lenght)
                checksum = self._uart.read()
                local_checksum = self._calculate_checksum(payload=payload)
                if checksum == local_checksum:
                    logging.info(f"Payload {payload} added to queue {self._input_queue.qsize() + 1}")
                    self._input_queue.put(payload)
            
            sleep(0.01)
            